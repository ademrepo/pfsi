@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_advanced_view(request):
    import traceback
    try:
        start_dt, end_dt = _parse_period(request)
        prev_end = start_dt
        prev_start = start_dt - (end_dt - start_dt)

        exp_current_qs = Expedition.objects.filter(date_creation__date__gte=start_dt, date_creation__date__lte=end_dt)
        exp_prev_qs = Expedition.objects.filter(date_creation__date__gte=prev_start, date_creation__date__lt=prev_end)
        fac_current_qs = Facture.objects.filter(date_facture__gte=start_dt, date_facture__lte=end_dt)
        fac_prev_qs = Facture.objects.filter(date_facture__gte=prev_start, date_facture__lt=prev_end)
        tour_current_qs = Tournee.objects.filter(date_tournee__gte=start_dt, date_tournee__lte=end_dt)
        tour_prev_qs = Tournee.objects.filter(date_tournee__gte=prev_start, date_tournee__lt=prev_end)
        incident_current_qs = Incident.objects.filter(created_at__date__gte=start_dt, created_at__date__lte=end_dt)
        incident_prev_qs = Incident.objects.filter(created_at__date__gte=prev_start, created_at__date__lt=prev_end)

        def _forecast(series, key):
            vals = [s[key] for s in series if s.get(key) is not None]
            if len(vals) < 3:
                return []
            window = vals[-3:]
            avg = sum(window) / 3.0
            last_month = datetime.date.fromisoformat(series[-1]['month'])
            out = []
            cur = last_month
            for _ in range(3):
                if cur.month == 12:
                    cur = datetime.date(cur.year + 1, 1, 1)
                else:
                    cur = datetime.date(cur.year, cur.month + 1, 1)
                out.append({'month': cur.isoformat(), key: round(float(avg), 2)})
            return out

        shipments_total = exp_current_qs.count()
        shipments_prev = exp_prev_qs.count()
        shipments_growth = _growth_rate(shipments_total, shipments_prev)

        delivered = exp_current_qs.filter(statut='Livré').count()
        failed = exp_current_qs.filter(statut='Échec de livraison').count()
        delayed = exp_current_qs.filter(incidents__type_incident='RETARD').distinct().count()

        denom = delivered + failed
        success_rate = round((delivered / denom) * 100.0, 2) if denom else None
        failed_rate = round((failed / denom) * 100.0, 2) if denom else None
        delayed_rate = round((delayed / shipments_total) * 100.0, 2) if shipments_total else None

        shipments_by_month_rows = (
            exp_current_qs.annotate(month=TruncMonth('date_creation'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        shipments_series = _fill_month_series(shipments_by_month_rows, start_dt, end_dt, key='count')
        shipments_forecast = _forecast(shipments_series, 'count')

        revenue_total = fac_current_qs.aggregate(v=Sum('total_ttc'))['v'] or 0
        revenue_prev = fac_prev_qs.aggregate(v=Sum('total_ttc'))['v'] or 0
        revenue_growth = _growth_rate(revenue_total, revenue_prev)

        revenue_by_month_rows = (
            fac_current_qs.annotate(month=TruncMonth('date_facture'))
            .values('month')
            .annotate(total=Sum('total_ttc'))
            .order_by('month')
        )
        revenue_series = _fill_month_series(revenue_by_month_rows, start_dt, end_dt, key='total')
        revenue_forecast = _forecast(revenue_series, 'total')

        routes_completed_total = tour_current_qs.filter(statut='Terminée').count()
        routes_completed_prev = tour_prev_qs.filter(statut='Terminée').count()
        routes_growth = _growth_rate(routes_completed_total, routes_completed_prev)

        routes_by_month_rows = (
            tour_current_qs.filter(statut='Terminée')
            .annotate(month=TruncMonth('date_tournee'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        routes_series = _fill_month_series(routes_by_month_rows, start_dt, end_dt, key='count')
        routes_forecast = _forecast(routes_series, 'count')

        fuel_by_month_rows = (
            tour_current_qs.filter(statut='Terminée')
            .annotate(month=TruncMonth('date_tournee'))
            .values('month')
            .annotate(total=Sum('consommation_litres'))
            .order_by('month')
        )
        fuel_series = _fill_month_series(fuel_by_month_rows, start_dt, end_dt, key='total')
        fuel_forecast = _forecast(fuel_series, 'total')

        total_distance = tour_current_qs.filter(statut='Terminée').aggregate(v=Sum('distance_km'))['v'] or 0
        total_fuel = tour_current_qs.filter(statut='Terminée').aggregate(v=Sum('consommation_litres'))['v'] or 0
        fuel_per_100km = round((float(total_fuel) / float(total_distance)) * 100.0, 2) if total_distance else None

        incidents_total = incident_current_qs.count()
        incidents_prev = incident_prev_qs.count()
        incidents_growth = _growth_rate(incidents_total, incidents_prev)

        incidents_by_month_rows = (
            incident_current_qs.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        incidents_series = _fill_month_series(incidents_by_month_rows, start_dt, end_dt, key='count')
        incidents_forecast = _forecast(incidents_series, 'count')


        incident_zones = (
            incident_current_qs.filter(expedition__isnull=False)
            .values('expedition__destination__zone_geographique')
            .annotate(incidents=Count('id'))
            .order_by('-incidents')
        )
        incident_zones = [
            {'zone': r['expedition__destination__zone_geographique'] or 'N/A', 'incidents': r['incidents']}
            for r in incident_zones
        ]

        top_zones_by_shipments = (
            exp_current_qs.values('destination__zone_geographique')
            .annotate(shipments=Count('id'))
            .order_by('-shipments')[:10]
        )
        top_zones_by_shipments = [
            {'zone': r['destination__zone_geographique'] or 'N/A', 'shipments': r['shipments']}
            for r in top_zones_by_shipments
        ]

        top_zones_by_incidents = incident_zones[:10]


        peak_months = sorted(shipments_series, key=lambda x: x['count'], reverse=True)[:6]


        top_customers_volume = (
            exp_current_qs.values('client_id', 'client__nom', 'client__prenom')
            .annotate(shipments=Count('id'))
            .order_by('-shipments')[:10]
        )
        top_customers_volume = [
            {
                'client_id': r['client_id'],
                'client_name': (f"{r['client__nom']} {r['client__prenom']}".strip() if r['client__prenom'] else r['client__nom']),
                'shipments': r['shipments'],
            }
            for r in top_customers_volume
            if r['client_id'] is not None
        ]


        top_customers_revenue = (
            fac_current_qs.values('client_id', 'client__nom', 'client__prenom')
            .annotate(revenue=Sum('total_ttc'))
            .order_by('-revenue')[:10]
        )
        top_customers_revenue = [
            {
                'client_id': r['client_id'],
                'client_name': (f"{r['client__nom']} {r['client__prenom']}".strip() if r['client__prenom'] else r['client__nom']),
                'revenue': float(r['revenue'] or 0),
            }
            for r in top_customers_revenue
            if r['client_id'] is not None
        ]

        top_destinations = (
            exp_current_qs.values(
                'destination_id',
                'destination__ville',
                'destination__pays',
                'destination__zone_geographique',
                'destination__latitude',
                'destination__longitude',
            )
            .annotate(shipments=Count('id'))
            .order_by('-shipments')[:10]
        )
        top_destinations = [
            {
                'destination_id': r['destination_id'],
                'label': f"{r['destination__ville']}, {r['destination__pays']}",
                'zone': r['destination__zone_geographique'],
                'shipments': r['shipments'],
                'latitude': r['destination__latitude'],
                'longitude': r['destination__longitude'],
            }
            for r in top_destinations
            if r['destination_id'] is not None
        ]

        driver_rows = (
            tour_current_qs.filter(statut='Terminée', chauffeur__isnull=False)
            .values('chauffeur_id', 'chauffeur__nom', 'chauffeur__prenom')
            .annotate(
                tournees=Count('id'),
                distance=Sum('distance_km'),
                fuel=Sum('consommation_litres'),
                duree=Sum('duree_minutes'),
                incidents=Count('incidents', distinct=True),
                delivered_shipments=Count('expeditions', filter=Q(expeditions__statut='Livré'), distinct=True),
                failed_shipments=Count('expeditions', filter=Q(expeditions__statut='Échec de livraison'), distinct=True),
                delayed_shipments=Count('expeditions', filter=Q(expeditions__incidents__type_incident='RETARD'), distinct=True),
            )
            .order_by('-tournees')[:20]
        )
        top_drivers = []
        for r in driver_rows:
            tours = float(r['tournees'] or 0)
            incidents = float(r['incidents'] or 0)
            distance = float(r['distance'] or 0)
            fuel = float(r['fuel'] or 0)
            duree_min = float(r['duree'] or 0)
            delivered_shipments = float(r['delivered_shipments'] or 0)
            failed_shipments = float(r['failed_shipments'] or 0)
            delayed_shipments = float(r['delayed_shipments'] or 0)

            speed_kmh = round((distance / (duree_min / 60.0)), 2) if duree_min else None
            deliveries_per_100km = round((delivered_shipments / distance) * 100.0, 2) if distance else None
            deliveries_per_liter = round((delivered_shipments / fuel), 2) if fuel else None
            punctuality_proxy = round((delivered_shipments / (delivered_shipments + delayed_shipments)) * 100.0, 2) if (delivered_shipments + delayed_shipments) else None
            quality_proxy = round((delivered_shipments / (delivered_shipments + failed_shipments)) * 100.0, 2) if (delivered_shipments + failed_shipments) else None

            score = (tours * 1.0) + (delivered_shipments * 0.2) - (incidents * 0.8) - (failed_shipments * 0.6) - (delayed_shipments * 0.3)
            top_drivers.append({
                'chauffeur_id': r['chauffeur_id'],
                'name': f"{r['chauffeur__nom']} {r['chauffeur__prenom']}",
                'tournees_completed': int(tours),
                'distance_km': distance,
                'fuel_l': fuel,
                'incidents': int(incidents),
                'delivered_shipments': int(delivered_shipments),
                'failed_shipments': int(failed_shipments),
                'delayed_shipments': int(delayed_shipments),
                'speed_kmh': speed_kmh,
                'deliveries_per_100km': deliveries_per_100km,
                'deliveries_per_liter': deliveries_per_liter,
                'punctuality_percent': punctuality_proxy,
                'quality_percent': quality_proxy,
                'score': round(float(score), 2),
            })
        top_drivers = sorted(top_drivers, key=lambda x: x['score'], reverse=True)[:10]

        fuel_price_per_liter = float(request.query_params.get('fuel_price_per_liter', 1.5))
        driver_cost_per_hour = float(request.query_params.get('driver_cost_per_hour', 8.0))
        vehicle_cost_per_km = float(request.query_params.get('vehicle_cost_per_km', 0.3))


        route_cost_total = 0.0
        for t in tour_current_qs.filter(statut='Terminée').only('distance_km', 'duree_minutes', 'consommation_litres'):
            dist = float(t.distance_km or 0)
            fuel_l = float(t.consommation_litres or 0)
            minutes = float(t.duree_minutes or 0)
            route_cost_total += (fuel_l * fuel_price_per_liter) + ((minutes / 60.0) * driver_cost_per_hour) + (dist * vehicle_cost_per_km)

        avg_cost_per_route = round((route_cost_total / routes_completed_total), 2) if routes_completed_total else None
        avg_shipments_per_route = round((shipments_total / routes_completed_total), 2) if routes_completed_total else None

        revenue_estimated = exp_current_qs.aggregate(v=Sum('montant_total'))['v'] or 0
        profit_estimated = round(float(revenue_estimated) - float(route_cost_total), 2)
        margin_percent = round((profit_estimated / float(revenue_estimated)) * 100.0, 2) if revenue_estimated else None

        revenue_by_service_rows = (
            exp_current_qs.values('type_service_id', 'type_service__libelle')
            .annotate(revenue=Sum('montant_total'), shipments=Count('id'))
            .order_by('-revenue')
        )
        profitability_by_service = []
        for r in revenue_by_service_rows:
            share = (float(r['revenue'] or 0) / float(revenue_estimated)) if revenue_estimated else 0
            cost_alloc = route_cost_total * share
            rev = float(r['revenue'] or 0)
            prof = rev - cost_alloc
            profitability_by_service.append({
                'type_service_id': r['type_service_id'],
                'type_service': r['type_service__libelle'] or 'N/A',
                'shipments': r['shipments'],
                'revenue_estimated': round(rev, 2),
                'cost_estimated': round(float(cost_alloc), 2),
                'profit_estimated': round(float(prof), 2),
                'margin_percent': round((prof / rev) * 100.0, 2) if rev else None,
            })


        cap_shipments_per_vehicle_per_day = float(request.query_params.get('cap_shipments_per_vehicle_per_day', 30))
        cap_shipments_per_driver_per_day = float(request.query_params.get('cap_shipments_per_driver_per_day', 25))
        working_days_per_month = float(request.query_params.get('working_days_per_month', 22))

        def _staffing_from_monthly_shipments(monthly_shipments):
            denom_vehicle = cap_shipments_per_vehicle_per_day * working_days_per_month
            denom_driver = cap_shipments_per_driver_per_day * working_days_per_month
            vehicles = math.ceil(monthly_shipments / denom_vehicle) if denom_vehicle else None
            drivers = math.ceil(monthly_shipments / denom_driver) if denom_driver else None
            return vehicles, drivers

        staffing_forecast = []
        for row in shipments_forecast:
            m = row['month']
            vol = float(row['count'] or 0)
            vehicles, drivers = _staffing_from_monthly_shipments(vol)
            staffing_forecast.append({
                'month': m,
                'forecast_shipments': round(vol, 2),
                'required_vehicles': vehicles,
                'required_drivers': drivers,
            })

        destination_points = (
            exp_current_qs.values(
                'destination_id',
                'destination__ville',
                'destination__pays',
                'destination__zone_geographique',
                'destination__latitude',
                'destination__longitude',
            )
            .annotate(shipments=Count('id'), incidents=Count('incidents', distinct=True))
            .order_by('-shipments')
        )
        destination_points = [
            {
                'destination_id': r['destination_id'],
                'label': f"{r['destination__ville']}, {r['destination__pays']}",
                'zone': r['destination__zone_geographique'],
                'latitude': r['destination__latitude'],
                'longitude': r['destination__longitude'],
                'shipments': r['shipments'],
                'incidents': r['incidents'],
            }
            for r in destination_points
            if r['destination_id'] is not None and r['destination__latitude'] is not None and r['destination__longitude'] is not None
        ]

        return Response({
            'period': {'start': start_dt.isoformat(), 'end': end_dt.isoformat()},
            'shipments': {
                'total': shipments_total,
                'growth_rate_percent': shipments_growth,
                'delivered': delivered,
                'failed': failed,
                'delayed': delayed,
                'success_rate_percent': success_rate,
                'failed_rate_percent': failed_rate,
                'delayed_rate_percent': delayed_rate,
                'series': shipments_series,
                'forecast_next_3_months': shipments_forecast,
            },
            'revenue': {
                'total_ttc': round(float(revenue_total), 2),
                'growth_rate_percent': revenue_growth,
                'series': revenue_series,
                'forecast_next_3_months': revenue_forecast,
            },
            'routes': {
                'completed': routes_completed_total,
                'growth_rate_percent': routes_growth,
                'series': routes_series,
                'forecast_next_3_months': routes_forecast,
            },
            'fuel': {
                'total_liters': round(float(total_fuel), 2),
                'fuel_per_100km': fuel_per_100km,
                'series': fuel_series,
                'forecast_next_3_months': fuel_forecast,
            },
            'incidents': {
                'total': incidents_total,
                'growth_rate_percent': incidents_growth,
                'series': incidents_series,
                'forecast_next_3_months': incidents_forecast,
                'by_zone': incident_zones,
            },
            'operations': {
                'avg_cost_per_route_estimated': avg_cost_per_route,
                'avg_shipments_per_route': avg_shipments_per_route,
            },
            'profitability': {
                'assumptions': {
                    'fuel_price_per_liter': fuel_price_per_liter,
                    'driver_cost_per_hour': driver_cost_per_hour,
                    'vehicle_cost_per_km': vehicle_cost_per_km,
                },
                'revenue_estimated_from_shipments': round(float(revenue_estimated), 2),
                'cost_estimated_from_routes': round(float(route_cost_total), 2),
                'profit_estimated': profit_estimated,
                'margin_percent': margin_percent,
                'by_service_type': profitability_by_service,
            },
            'rankings': {
                'top_customers_by_volume': top_customers_volume,
                'top_customers_by_revenue': top_customers_revenue,
                'top_destinations': top_destinations,
                'top_drivers': top_drivers,
            },
            'staffing': {
                'assumptions': {
                    'cap_shipments_per_vehicle_per_day': cap_shipments_per_vehicle_per_day,
                    'cap_shipments_per_driver_per_day': cap_shipments_per_driver_per_day,
                    'working_days_per_month': working_days_per_month,
                },
                'forecast_next_3_months': staffing_forecast,
            },
            'map': {
                'destination_points': destination_points,
            },
            'zones': {
                'top_by_shipments': top_zones_by_shipments,
                'top_by_incidents': top_zones_by_incidents,
            },
            'peaks': {
                'months': peak_months,
            },
        })
    except Exception as e:
        print("[ANALYTICS ADVANCED ERROR]")
        traceback.print_exc()
        raise
