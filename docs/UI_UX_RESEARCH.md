# UI/UX Research - Bitcoin Wallet Design Patterns

## Overview
Analysis of UI/UX patterns from Bitcoin wallet projects to improve our frontend design, user experience, and visual appeal.

## Research Sources

### 1. eigenwallet/core (UnstoppableSwap)
**Focus**: Desktop GUI for atomic swaps  
**Key UI Patterns**:

#### Design Philosophy
- Clean, professional interface
- Clear status indicators
- Real-time updates
- Connection status visualization
- Peer-to-peer connection management

#### UI Components
- **Status Badges**: Clear visual indicators for swap status
- **Connection Indicators**: Show peer connection status
- **Progress Indicators**: Visual feedback for operations
- **Error States**: Clear error messages with recovery options

**Applicable Patterns**:
- Status indicators (we have these, can enhance)
- Connection/health indicators
- Progress feedback
- Error recovery UI

### 2. Bitcoin Design System (bitcoin.design)
**Focus**: Official Bitcoin design guidelines  
**Key Patterns**:

#### Color Scheme
- **Primary**: Orange/Gold (#F7931A - Bitcoin orange)
- **Success**: Green (#00D9A5)
- **Warning**: Amber/Yellow (#FFB800)
- **Error**: Red (#FF3B30)
- **Neutral**: Grays for backgrounds and text

#### Typography
- Clear, readable fonts
- Hierarchical text sizing
- Monospace for addresses/numbers

#### Components
- **Buttons**: Clear hierarchy, consistent sizing
- **Forms**: Clear labels, helpful hints
- **Cards**: Elevated design with shadows
- **Status Indicators**: Color-coded badges

**Applicable Patterns**:
- Bitcoin orange accent color
- Consistent color system
- Typography hierarchy
- Component patterns

### 3. BTCPay Server
**Focus**: Production payment processor UI  
**Key Patterns**:

#### Navigation
- Clear top navigation
- Breadcrumbs for deep navigation
- Sidebar for settings/configuration

#### Dashboard Design
- Statistics cards
- Recent activity feed
- Quick actions
- Visual charts/graphs

#### Settings/Profile
- Organized settings sections
- Clear form layouts
- Help text and tooltips

**Applicable Patterns**:
- Dashboard layout
- Settings organization
- Profile management
- Navigation patterns

### 4. General Bitcoin Wallet Patterns

#### Common UI Elements
1. **Balance Display**
   - Large, prominent balance
   - Currency toggle (BTC/sats)
   - Secondary currency (USD/EUR)

2. **Transaction History**
   - List view with filters
   - Status indicators
   - Date grouping

3. **Send/Receive**
   - QR code generation
   - Address input with validation
   - Amount input with currency conversion

4. **Security Features**
   - Lock/unlock indicators
   - Backup status
   - Security settings

## Design System Recommendations

### Color Palette

#### Primary Colors
```css
/* Bitcoin Orange (Primary) */
--bitcoin-orange: #F7931A;
--bitcoin-orange-dark: #E8820A;
--bitcoin-orange-light: #FFA64D;

/* Success Green */
--success: #10B981;
--success-dark: #059669;
--success-light: #34D399;

/* Warning Amber */
--warning: #F59E0B;
--warning-dark: #D97706;
--warning-light: #FBBF24;

/* Error Red */
--error: #EF4444;
--error-dark: #DC2626;
--error-light: #F87171;

/* Neutral Grays */
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-200: #E5E7EB;
--gray-300: #D1D5DB;
--gray-400: #9CA3AF;
--gray-500: #6B7280;
--gray-600: #4B5563;
--gray-700: #374151;
--gray-800: #1F2937;
--gray-900: #111827;
```

#### Dark Mode Colors
```css
/* Dark Mode Palette */
--dark-bg: #0F172A;
--dark-surface: #1E293B;
--dark-border: #334155;
--dark-text: #F1F5F9;
--dark-text-muted: #94A3B8;
```

### Typography

#### Font Hierarchy
- **Headings**: Bold, clear hierarchy (H1: 3xl, H2: 2xl, H3: xl)
- **Body**: Readable size (base: 16px)
- **Small Text**: 14px for hints, labels
- **Monospace**: For Bitcoin addresses, numbers

#### Font Families
- **Sans-serif**: System fonts for UI
- **Monospace**: 'Courier New', 'Monaco' for addresses

### Component Patterns

#### Buttons
- **Primary**: Bitcoin orange background
- **Secondary**: Outline with orange border
- **Destructive**: Red for delete actions
- **Ghost**: Minimal for secondary actions

#### Cards
- White background with subtle shadow
- Rounded corners (8px)
- Hover effects for interactivity
- Clear borders for separation

#### Status Badges
- **Active**: Green background
- **Inactive**: Gray background
- **Pending**: Amber background
- **Error**: Red background

#### Forms
- Clear labels above inputs
- Helpful placeholder text
- Real-time validation feedback
- Error messages below inputs

## UI Improvements to Implement

### 1. Enhanced Color Scheme
- [ ] Add Bitcoin orange as primary accent
- [ ] Implement consistent color system
- [ ] Add dark mode support (currently partial)
- [ ] Improve contrast ratios

### 2. Navigation Enhancements
- [ ] Add breadcrumbs for deep navigation
- [ ] Improve back button visibility
- [ ] Add navigation menu/sidebar
- [ ] Mobile-friendly navigation

### 3. Dashboard Improvements
- [ ] Add statistics cards with icons
- [ ] Improve chart visualization
- [ ] Add quick action buttons
- [ ] Recent activity feed

### 4. Component Enhancements
- [ ] Enhanced status badges
- [ ] Better loading states
- [ ] Improved empty states
- [ ] Better error states

### 5. User Experience
- [ ] Tooltips for complex features
- [ ] Help text in forms
- [ ] Confirmation dialogs
- [ ] Success animations

### 6. Settings/Profile (Future)
- [ ] User profile page
- [ ] Settings page
- [ ] Theme selector (light/dark)
- [ ] Preferences management

## Specific Patterns to Adopt

### From Bitcoin Design System

#### 1. Address Display Pattern
```tsx
// Bitcoin addresses should be:
// - Monospace font
// - Truncated with ellipsis
// - Copy button always visible
// - QR code option
```

#### 2. Balance Display Pattern
```tsx
// Large, prominent display
// Currency toggle (BTC/sats)
// Secondary currency conversion
// Clear formatting
```

#### 3. Status Indicator Pattern
```tsx
// Color-coded badges
// Icon + text
// Clear visual hierarchy
// Consistent across app
```

### From BTCPay Server

#### 1. Dashboard Layout
- Statistics cards at top
- Main content below
- Sidebar for navigation (optional)
- Clear visual hierarchy

#### 2. Settings Organization
- Grouped by category
- Clear section headers
- Help text for each setting
- Save/cancel buttons

### From eigenwallet/core

#### 1. Connection Status
- Visual indicators for system health
- Real-time status updates
- Clear error messages
- Recovery suggestions

#### 2. Progress Feedback
- Loading states for operations
- Progress bars for long operations
- Success/error animations
- Clear completion states

## Implementation Priority

### High Priority (Immediate)
1. ✅ Bitcoin orange accent color
2. ✅ Enhanced status badges
3. ✅ Improved button contrast (already done)
4. ⚠️ Better navigation visibility
5. ⚠️ Enhanced empty states

### Medium Priority (Next Sprint)
1. Dark mode toggle
2. Dashboard statistics cards
3. Tooltips and help text
4. Enhanced loading states
5. Better error states

### Low Priority (Future)
1. User profile page
2. Settings page
3. Theme customization
4. Advanced navigation
5. Animations and transitions

## Design Tokens

### Spacing
- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px

### Border Radius
- **sm**: 4px
- **md**: 8px
- **lg**: 12px
- **xl**: 16px
- **full**: 9999px

### Shadows
- **sm**: 0 1px 2px rgba(0,0,0,0.05)
- **md**: 0 4px 6px rgba(0,0,0,0.1)
- **lg**: 0 10px 15px rgba(0,0,0,0.1)
- **xl**: 0 20px 25px rgba(0,0,0,0.1)

## Accessibility Considerations

### Color Contrast
- Ensure WCAG AA compliance (4.5:1 for text)
- Test all color combinations
- Provide alternative indicators (icons + color)

### Keyboard Navigation
- All interactive elements keyboard accessible
- Clear focus indicators
- Logical tab order

### Screen Readers
- Proper ARIA labels
- Semantic HTML
- Alt text for images
- Form labels properly associated

## References

- [Bitcoin Design System](https://bitcoin.design/) - Official Bitcoin design guidelines
- [eigenwallet/core](https://github.com/eigenwallet/core) - Desktop GUI patterns
- [BTCPay Server](https://github.com/btcpayserver/btcpayserver) - Production UI patterns
- [Bitcoin Core GUI](https://github.com/bitcoin/bitcoin) - Reference implementation

