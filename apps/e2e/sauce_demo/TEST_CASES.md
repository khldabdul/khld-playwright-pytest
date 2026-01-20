# Test Cases: Sauce Demo (E2E)

**URL**: https://www.saucedemo.com/  
**Type**: E-commerce Flow  
**Priority**: 🥇 First to implement

---

## Test Users (Provided by Site)

| Username | Password | Behavior |
|----------|----------|----------|
| `standard_user` | `secret_sauce` | Normal user |
| `locked_out_user` | `secret_sauce` | Locked account - login fails |
| `problem_user` | `secret_sauce` | Has UI bugs |
| `performance_glitch_user` | `secret_sauce` | Slow responses |
| `error_user` | `secret_sauce` | Triggers errors |
| `visual_user` | `secret_sauce` | Visual differences |

---

## Test Suite: Authentication

### TC-SD-001: Successful Login
- **Priority**: Critical
- **Steps**:
  1. Navigate to login page
  2. Enter `standard_user` / `secret_sauce`
  3. Click Login button
- **Expected**: Redirected to inventory page, products visible

### TC-SD-002: Invalid Password
- **Priority**: High
- **Steps**:
  1. Navigate to login page
  2. Enter `standard_user` / `wrong_password`
  3. Click Login
- **Expected**: Error message "Username and password do not match"

### TC-SD-003: Locked Out User
- **Priority**: High
- **Steps**:
  1. Navigate to login page
  2. Enter `locked_out_user` / `secret_sauce`
  3. Click Login
- **Expected**: Error message "Sorry, this user has been locked out"

### TC-SD-004: Empty Credentials
- **Priority**: Medium
- **Steps**:
  1. Navigate to login page
  2. Leave username and password empty
  3. Click Login
- **Expected**: Error message about required username

---

## Test Suite: Inventory

### TC-SD-010: View All Products
- **Priority**: Critical
- **Steps**:
  1. Login as standard_user
  2. Observe inventory page
- **Expected**: 6 products displayed with name, price, image, description

### TC-SD-011: Sort Products by Price (Low to High)
- **Priority**: Medium
- **Steps**:
  1. Login as standard_user
  2. Select "Price (low to high)" from dropdown
- **Expected**: Products sorted ascending by price ($7.99 first)

### TC-SD-012: Sort Products by Name (Z to A)
- **Priority**: Medium
- **Steps**:
  1. Login as standard_user
  2. Select "Name (Z to A)" from dropdown
- **Expected**: Products sorted descending alphabetically

### TC-SD-013: Add Product to Cart
- **Priority**: Critical
- **Steps**:
  1. Login as standard_user
  2. Click "Add to cart" on first product
- **Expected**: Button changes to "Remove", cart badge shows "1"

### TC-SD-014: View Product Details
- **Priority**: Medium
- **Steps**:
  1. Login as standard_user
  2. Click on product name/image
- **Expected**: Navigate to product detail page with full description

---

## Test Suite: Shopping Cart

### TC-SD-020: Add Multiple Products
- **Priority**: High
- **Steps**:
  1. Login as standard_user
  2. Add 3 different products to cart
- **Expected**: Cart badge shows "3"

### TC-SD-021: View Cart Contents
- **Priority**: Critical
- **Steps**:
  1. Add products to cart
  2. Click cart icon
- **Expected**: Cart page shows all added products with prices

### TC-SD-022: Remove Product from Cart
- **Priority**: High
- **Steps**:
  1. Add product to cart
  2. Go to cart
  3. Click "Remove" button
- **Expected**: Product removed, cart updated

### TC-SD-023: Continue Shopping
- **Priority**: Medium
- **Steps**:
  1. Go to cart page
  2. Click "Continue Shopping"
- **Expected**: Return to inventory page

---

## Test Suite: Checkout

### TC-SD-030: Complete Checkout Flow
- **Priority**: Critical
- **Steps**:
  1. Add products to cart
  2. Go to cart, click "Checkout"
  3. Fill in: First Name, Last Name, Postal Code
  4. Click Continue
  5. Verify order summary
  6. Click Finish
- **Expected**: "Thank you for your order!" confirmation

### TC-SD-031: Checkout Validation - Empty Fields
- **Priority**: High
- **Steps**:
  1. Go to checkout
  2. Leave fields empty
  3. Click Continue
- **Expected**: Error message about required first name

### TC-SD-032: Verify Order Total
- **Priority**: Critical
- **Steps**:
  1. Add specific products ($29.99 + $9.99)
  2. Checkout to summary page
- **Expected**: Subtotal $39.98, Tax calculated, Total displayed

### TC-SD-033: Cancel Checkout
- **Priority**: Medium
- **Steps**:
  1. Go to checkout
  2. Click Cancel
- **Expected**: Return to cart page

---

## Test Suite: Navigation & Session

### TC-SD-040: Logout
- **Priority**: High
- **Steps**:
  1. Login as standard_user
  2. Open hamburger menu
  3. Click "Logout"
- **Expected**: Redirected to login page

### TC-SD-041: Reset App State
- **Priority**: Medium
- **Steps**:
  1. Login, add items to cart
  2. Open menu, click "Reset App State"
- **Expected**: Cart cleared, all "Add to cart" buttons restored

---

## Page Objects Required

| Page Object | Key Elements |
|-------------|--------------|
| `LoginPage` | username, password, login_button, error_message |
| `InventoryPage` | product_list, sort_dropdown, cart_badge, add_to_cart_buttons |
| `ProductDetailPage` | product_name, price, description, add_to_cart, back_button |
| `CartPage` | cart_items, checkout_button, continue_shopping, remove_buttons |
| `CheckoutStepOnePage` | first_name, last_name, postal_code, continue_button, cancel |
| `CheckoutStepTwoPage` | item_summary, subtotal, tax, total, finish_button |
| `CheckoutCompletePage` | success_message, back_home_button |
