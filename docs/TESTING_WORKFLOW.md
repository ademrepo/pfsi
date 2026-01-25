# Testing Workflow Guide

This document provides comprehensive instructions for testing the PFKHRA application, including backend API tests, frontend component tests, and integration testing procedures.

## Table of Contents

1. [Backend Testing](#backend-testing)
2. [Frontend Testing](#frontend-testing)
3. [Integration Testing](#integration-testing)
4. [Test Data Management](#test-data-management)
5. [Continuous Integration](#continuous-integration)
6. [Debugging and Troubleshooting](#debugging-and-troubleshooting)

## Backend Testing

### Running Backend Tests

The backend uses Django's built-in testing framework. Tests are located in the `backend/core/tests.py` file.

#### 1. Basic Test Execution

```bash
# Navigate to backend directory
cd backend

# Run all tests
python manage.py test

# Run specific test class
python manage.py test core.tests.AnalyticsTestCase

# Run specific test method
python manage.py test core.tests.AnalyticsTestCase.test_analytics_endpoint_success
```

#### 2. Analytics-Specific Tests

The analytics endpoint has dedicated tests in `backend/test_analytics.py`:

```bash
# Run analytics tests specifically
python test_analytics.py

# Or run through Django test runner
python manage.py test test_analytics
```

#### 3. Test Coverage

To check test coverage:

```bash
# Install coverage if not already installed
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML coverage report
```

### Test Categories

#### Unit Tests
- **Model Tests**: Test database models and relationships
- **Serializer Tests**: Test data serialization/deserialization
- **View Tests**: Test API endpoints and business logic
- **Permission Tests**: Test authentication and authorization

#### Integration Tests
- **API Endpoint Tests**: Test complete API workflows
- **Database Integration**: Test database operations
- **Authentication Flow**: Test login/logout workflows

### Test Data Setup

#### Test Fixtures

Test data is automatically created using Django fixtures. The test database is isolated from production data.

```python
# Example test setup in tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Client, Expedition, Chauffeur

class AnalyticsTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )
        
        # Create test data
        self.client = Client.objects.create(
            nom='Test Client',
            adresse='123 Test St',
            telephone='1234567890'
        )
        
        # Create test expeditions
        Expedition.objects.create(
            client=self.client,
            destination='Test Destination',
            poids=10.5,
            statut='delivered'
        )
```

## Frontend Testing

### Running Frontend Tests

The frontend uses React with Vite. Tests are located in the `frontend/src` directory.

#### 1. Basic Test Execution

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

#### 2. Component Testing

Components are tested using React Testing Library:

```javascript
// Example test in src/components/__tests__/Analytics.test.js
import { render, screen, waitFor } from '@testing-library/react';
import Analytics from '../pages/Analytics';
import { AuthProvider } from '../contexts/AuthContext';

describe('Analytics Component', () => {
    test('renders analytics dashboard', async () => {
        render(
            <AuthProvider>
                <Analytics />
            </AuthProvider>
        );
        
        await waitFor(() => {
            expect(screen.getByText('Analytics Dashboard')).toBeInTheDocument();
        });
    });
});
```

### Test Categories

#### Unit Tests
- **Component Tests**: Test individual React components
- **Hook Tests**: Test custom hooks and state management
- **Utility Tests**: Test helper functions and utilities

#### Integration Tests
- **Page Tests**: Test complete page rendering
- **API Integration**: Test API calls and data fetching
- **User Interaction**: Test user interactions and state changes

## Integration Testing

### End-to-End Testing

#### 1. Manual Testing Workflow

1. **Start Backend Server**:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Start Frontend Development Server**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test User Scenarios**:
   - Login with different user roles
   - Navigate through all pages
   - Test CRUD operations
   - Verify analytics dashboard functionality

#### 2. Automated E2E Testing

Using tools like Cypress or Playwright:

```bash
# Install Cypress
npm install cypress --save-dev

# Run E2E tests
npx cypress run

# Open Cypress Test Runner
npx cypress open
```

### Test Scenarios

#### Admin User Scenarios
1. Login as admin
2. Access analytics dashboard
3. View all metrics
4. Test data refresh
5. Verify export functionality

#### Agent User Scenarios
1. Login as agent
2. Create new expeditions
3. Update expedition status
4. Generate invoices
5. Process payments

#### Client User Scenarios
1. Login as client
2. View expedition history
3. Check invoice status
4. Submit reclamations

## Test Data Management

### Test Database

#### Django Test Database
- Django automatically creates a separate test database
- Test data is isolated and cleaned up after tests
- Use `--keepdb` flag to preserve test database between runs

```bash
# Run tests with preserved database
python manage.py test --keepdb
```

#### Test Data Factories

Use factory classes to generate test data:

```python
# In factories.py
import factory
from django.contrib.auth.models import User
from core.models import Client, Expedition

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    is_staff = False

class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client
    
    nom = factory.Faker('name')
    adresse = factory.Faker('address')
    telephone = factory.Faker('phone_number')
```

### Test Data Cleanup

#### Automatic Cleanup
- Django tests automatically clean up test data
- Use `tearDown()` method for manual cleanup if needed

#### Manual Cleanup
```python
def tearDown(self):
    # Clean up test data
    User.objects.all().delete()
    Client.objects.all().delete()
    Expedition.objects.all().delete()
```

## Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Test Workflow

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run backend tests
      run: |
        cd backend
        python manage.py test
    
    - name: Run coverage
      run: |
        cd backend
        coverage run --source='.' manage.py test
        coverage report

  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'
    
    - name: Install dependencies
      run: |
        cd frontend
        npm install
    
    - name: Run frontend tests
      run: npm test -- --coverage --watchAll=false
    
    - name: Build frontend
      run: npm run build

  integration-tests:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    
    - name: Set up Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        cd ../frontend
        npm install
    
    - name: Run integration tests
      run: |
        # Start backend server
        cd backend
        python manage.py runserver &
        sleep 5
        
        # Start frontend and run tests
        cd ../frontend
        npm run test:integration
```

### Pre-commit Hooks

Set up pre-commit hooks to run tests before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: local
    hooks:
      - id: backend-tests
        name: Run backend tests
        entry: cd backend && python manage.py test
        language: system
        pass_filenames: false
        always_run: true
      
      - id: frontend-tests
        name: Run frontend tests
        entry: cd frontend && npm test
        language: system
        pass_filenames: false
        always_run: true
EOF

# Install pre-commit hooks
pre-commit install
```

## Debugging and Troubleshooting

### Common Issues

#### Backend Test Issues
1. **Database Connection Errors**:
   ```bash
   # Check database configuration
   python manage.py check --database default
   
   # Reset migrations if needed
   python manage.py migrate --fake-initial
   ```

2. **Authentication Errors**:
   ```python
   # Ensure proper user creation in tests
   from django.contrib.auth.models import User
   
   def setUp(self):
       self.user = User.objects.create_user(
           username='testuser',
           password='testpass123'
       )
   ```

#### Frontend Test Issues
1. **Component Rendering Errors**:
   ```javascript
   // Mock external dependencies
   jest.mock('../api');
   
   // Use proper test providers
   const renderWithProviders = (component) => {
       return render(
           <AuthProvider>
               <Router>
                   {component}
               </Router>
           </AuthProvider>
       );
   };
   ```

2. **Async Test Issues**:
   ```javascript
   // Use proper async testing utilities
   import { waitFor } from '@testing-library/react';
   
   test('async operation', async () => {
       await waitFor(() => {
           expect(element).toBeInTheDocument();
       });
   });
   ```

### Debugging Tools

#### Backend Debugging
```python
# Add debug prints in tests
import logging
logging.basicConfig(level=logging.DEBUG)

# Use Django shell for debugging
python manage.py shell
```

#### Frontend Debugging
```javascript
// Add debug logs
console.log('Test data:', testData);

// Use React DevTools for component debugging
// Install React DevTools browser extension
```

### Test Performance Optimization

#### Backend Optimization
```python
# Use transaction.atomic() for faster tests
from django.db import transaction

@transaction.atomic
def setUp(self):
    # Create test data
    pass

# Use @override_settings for faster tests
from django.test import override_settings

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class MyTestCase(TestCase):
    pass
```

#### Frontend Optimization
```javascript
// Mock expensive operations
jest.mock('../api', () => ({
    fetchData: jest.fn(() => Promise.resolve(mockData))
}));

// Use shallow rendering for component tests
import { shallow } from 'enzyme';
```

## Best Practices

### Test Organization
1. **Follow naming conventions**: `test_*.py` for Python, `*.test.js` for JavaScript
2. **Group related tests**: Use test classes and describe blocks
3. **Use descriptive test names**: Clearly describe what each test does

### Test Data
1. **Use factories**: Create reusable test data factories
2. **Keep tests independent**: Each test should be able to run independently
3. **Use minimal test data**: Only create data needed for the specific test

### Test Maintenance
1. **Regular test reviews**: Review and update tests regularly
2. **Remove obsolete tests**: Delete tests for removed functionality
3. **Update test documentation**: Keep this guide updated with new testing procedures

### Code Coverage
1. **Aim for 80%+ coverage**: Target high but realistic coverage
2. **Focus on critical paths**: Prioritize testing business-critical functionality
3. **Use coverage reports**: Regularly review coverage reports to identify gaps

This testing workflow ensures the application remains reliable and maintainable as it grows and evolves.