# Test Cases: The Internet (E2E)

**URL**: https://the-internet.herokuapp.com/  
**Type**: Component Isolation Testing  
**Priority**: 🥈 Second to implement

---

## Overview

This site tests **isolated UI components** rather than a flow. Each page demonstrates a specific challenge.

---

## Test Suite: Authentication

### TC-TI-001: Basic Auth Success
- **URL**: `/basic_auth`
- **Steps**:
  1. Navigate with credentials in URL: `https://admin:admin@the-internet.herokuapp.com/basic_auth`
- **Expected**: Message "Congratulations! You must have the proper credentials."

### TC-TI-002: Form Authentication - Valid Login
- **URL**: `/login`
- **Steps**:
  1. Enter username: `tomsmith`
  2. Enter password: `SuperSecretPassword!`
  3. Click Login
- **Expected**: Success flash message, redirected to `/secure`

### TC-TI-003: Form Authentication - Invalid Login
- **URL**: `/login`
- **Steps**:
  1. Enter invalid credentials
  2. Click Login
- **Expected**: Error flash message "Your username is invalid!"

### TC-TI-004: Logout
- **URL**: `/secure`
- **Steps**:
  1. Login successfully
  2. Click Logout button
- **Expected**: Redirected to login, success logout message

---

## Test Suite: Form Elements

### TC-TI-010: Checkboxes - Toggle State
- **URL**: `/checkboxes`
- **Steps**:
  1. Navigate to checkboxes page
  2. Verify checkbox 1 is unchecked, checkbox 2 is checked
  3. Click both checkboxes
- **Expected**: States toggle (checkbox 1 checked, checkbox 2 unchecked)

### TC-TI-011: Dropdown Selection
- **URL**: `/dropdown`
- **Steps**:
  1. Navigate to dropdown page
  2. Select "Option 1"
  3. Verify selection
  4. Select "Option 2"
- **Expected**: Selected option visible in dropdown

### TC-TI-012: Inputs - Number Field
- **URL**: `/inputs`
- **Steps**:
  1. Navigate to inputs page
  2. Enter number "123"
  3. Use arrow keys to increment/decrement
- **Expected**: Number field accepts and adjusts values

---

## Test Suite: Dynamic Elements

### TC-TI-020: Dynamic Loading - Element Appears
- **URL**: `/dynamic_loading/1`
- **Steps**:
  1. Click Start button
  2. Wait for loading bar to complete
- **Expected**: "Hello World!" text appears

### TC-TI-021: Dynamic Loading - Element Rendered After
- **URL**: `/dynamic_loading/2`
- **Steps**:
  1. Click Start button
  2. Wait for element to be added to DOM
- **Expected**: "Hello World!" text appears (element didn't exist before)

### TC-TI-022: Add/Remove Elements
- **URL**: `/add_remove_elements/`
- **Steps**:
  1. Click "Add Element" 3 times
  2. Verify 3 Delete buttons appear
  3. Click one Delete button
- **Expected**: 2 Delete buttons remain

### TC-TI-023: Disappearing Elements
- **URL**: `/disappearing_elements`
- **Steps**:
  1. Navigate and count menu items
  2. Refresh page multiple times
- **Expected**: Sometimes 5 elements, sometimes 4 (Gallery may disappear)

---

## Test Suite: Interactions

### TC-TI-030: Drag and Drop
- **URL**: `/drag_and_drop`
- **Steps**:
  1. Drag column A to column B position
- **Expected**: Columns swap positions (A becomes B, B becomes A)

### TC-TI-031: Hover - Display Hidden Info
- **URL**: `/hovers`
- **Steps**:
  1. Hover over each user image
- **Expected**: User name and "View profile" link appears on hover

### TC-TI-032: Sortable Data Tables
- **URL**: `/tables`
- **Steps**:
  1. Click on "Last Name" column header
  2. Verify table sorts by last name
- **Expected**: Table data sorted alphabetically

---

## Test Suite: JavaScript Dialogs

### TC-TI-040: JS Alert
- **URL**: `/javascript_alerts`
- **Steps**:
  1. Click "Click for JS Alert"
  2. Accept the alert
- **Expected**: Result text shows "You successfully clicked an alert"

### TC-TI-041: JS Confirm - Accept
- **URL**: `/javascript_alerts`
- **Steps**:
  1. Click "Click for JS Confirm"
  2. Accept the confirm dialog
- **Expected**: Result shows "You clicked: Ok"

### TC-TI-042: JS Confirm - Dismiss
- **URL**: `/javascript_alerts`
- **Steps**:
  1. Click "Click for JS Confirm"
  2. Dismiss the confirm dialog
- **Expected**: Result shows "You clicked: Cancel"

### TC-TI-043: JS Prompt
- **URL**: `/javascript_alerts`
- **Steps**:
  1. Click "Click for JS Prompt"
  2. Enter text "Hello Playwright"
  3. Accept
- **Expected**: Result shows "You entered: Hello Playwright"

---

## Test Suite: Frames & Windows

### TC-TI-050: iFrame - TinyMCE Editor
- **URL**: `/iframe`
- **Steps**:
  1. Switch to iframe
  2. Clear existing text
  3. Type "Playwright test content"
- **Expected**: Text appears in TinyMCE editor

### TC-TI-051: Nested Frames
- **URL**: `/nested_frames`
- **Steps**:
  1. Navigate through top/bottom frames
  2. Read content from each frame (LEFT, MIDDLE, RIGHT, BOTTOM)
- **Expected**: Correct text from each nested frame

### TC-TI-052: Multiple Windows
- **URL**: `/windows`
- **Steps**:
  1. Click "Click Here" link
  2. Handle new window/tab
  3. Verify new window content
- **Expected**: New window has "New Window" heading

---

## Test Suite: Uploads & Downloads

### TC-TI-060: File Upload
- **URL**: `/upload`
- **Steps**:
  1. Upload a test file
  2. Click Upload button
- **Expected**: Filename displayed in result

### TC-TI-061: File Download
- **URL**: `/download`
- **Steps**:
  1. Click on a file link
  2. Handle download
- **Expected**: File downloaded successfully

---

## Test Suite: Edge Cases

### TC-TI-070: Broken Images
- **URL**: `/broken_images`
- **Steps**:
  1. Check all images on page
- **Expected**: Identify which images are broken (404)

### TC-TI-071: Challenging DOM
- **URL**: `/challenging_dom`
- **Steps**:
  1. Navigate to page with dynamic IDs
  2. Locate elements using stable selectors
- **Expected**: Elements found despite changing IDs

### TC-TI-072: Infinite Scroll
- **URL**: `/infinite_scroll`
- **Steps**:
  1. Scroll down multiple times
  2. Count loaded paragraphs
- **Expected**: New paragraphs load as you scroll

---

## Page Objects Required

| Page Object | Key Elements |
|-------------|--------------|
| `LoginPage` | username, password, login_button, flash_message |
| `SecurePage` | logout_button, success_message |
| `CheckboxesPage` | checkbox_1, checkbox_2 |
| `DropdownPage` | dropdown, options |
| `DragDropPage` | column_a, column_b |
| `AlertsPage` | alert_button, confirm_button, prompt_button, result |
| `FramesPage` | iframe, nested_frames |
| `UploadPage` | file_input, upload_button, result |
