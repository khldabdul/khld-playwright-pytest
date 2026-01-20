# Test Cases: Medusa Store (E2E)

**URL**: https://next.medusajs.com/us/store  
**Type**: Modern Next.js E-commerce  
**Priority**: 🥉 Third to implement

---

## Technical Notes

- **Framework**: Next.js / React
- **Dynamic DOM**: Heavy client-side rendering
- **Strategy**: Use `data-testid` when available, stable text selectors otherwise

---

## Test Suite: Navigation & Search

### TC-MS-001: Homepage Loads
- **Steps**:
  1. Navigate to store homepage
- **Expected**: Featured products visible

### TC-MS-003: Category Navigation
- **Steps**:
  1. Click on a category (e.g., "Merch")
- **Expected**: Category page loads with filtered products

---

## Test Suite: Product Browsing

### TC-MS-010: View Product Details
- **Steps**:
  1. Click on any product
- **Expected**: Product detail page with title, price, description, images

### TC-MS-011: Select Product Variant
- **Steps**:
  1. Open product with variants (size/color)
  2. Select different options
- **Expected**: Price/availability updates accordingly

### TC-MS-012: Image Gallery
- **Steps**:
  1. Open product with multiple images
  2. Click through gallery
- **Expected**: Images change correctly

---

## Test Suite: Shopping Cart

### TC-MS-020: Add to Cart
- **Steps**:
  1. Open product detail
  2. Select variant (if required)
  3. Click "Add to cart"
- **Expected**: Cart drawer opens, item added

### TC-MS-021: Update Cart Quantity
- **Steps**:
  1. Add item to cart
  2. Increase/decrease quantity
- **Expected**: Quantity and total update

### TC-MS-022: Remove from Cart
- **Steps**:
  1. Add item to cart
  2. Click remove button
- **Expected**: Item removed, cart updated

---

## Test Suite: Guest Checkout

### TC-MS-030: Checkout as Guest
- **Steps**:
  1. Add items to cart
  2. Proceed to checkout
  3. Enter shipping info
  4. Select payment method
  5. Complete order
- **Expected**: Order confirmation displayed

### TC-MS-031: Checkout Form Validation
- **Steps**:
  1. Go to checkout
  2. Submit with empty required fields
- **Expected**: Validation errors shown

---

## Test Suite: Complete Checkout Flow

### TC-MS-040: Guest Checkout with Invoice Generation
- **Steps**:
  1. Add item(s) to cart
  2. Click cart icon
  3. Click "Checkout" button
  4. **Shipping Information**:
     - Enter email address
     - Enter first name
     - Enter last name
     - Enter address
     - Enter city
     - Enter postal code
     - Select country/region
  5. Click "Continue to delivery"
  6. **Shipping Method**:
     - Select shipping option
  7. Click "Continue to payment"
  8. **Payment Information**:
     - Enter card details (test mode)
     - Enter billing address (if different)
  9. Click "Complete order"
  10. Wait for order confirmation
- **Expected**: 
  - Order confirmation page displays
  - Order number visible
  - Order summary/invoice shown
  - Email confirmation sent (if configured)

### TC-MS-041: Verify Order Confirmation Details
- **Steps**:
  1. Complete checkout (TC-MS-040)
  2. On confirmation page, verify:
     - Order number
     - Items purchased
     - Shipping address
     - Total amount
     - Payment method (last 4 digits)
- **Expected**: All order details match cart and checkout

---

## Test Suite: Region & Locale

### TC-MS-040: Switch Region
- **Steps**:
  1. Click region selector
  2. Switch from US to EU
- **Expected**: Currency changes (USD → EUR)

---

## Page Objects Required

| Page Object | Key Elements |
|-------------|--------------|
| `HomePage` | search_bar, featured_products, categories |
| `SearchResultsPage` | results_list, filters |
| `ProductPage` | title, price, variants, add_to_cart, gallery |
| `CartDrawer` | items, quantity, total, checkout_button |
| `CheckoutPage` | shipping_form, payment, place_order |
