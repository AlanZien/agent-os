# Frontend Patterns - {ProjectName}

**Version**: 1.0 | **Complement to**: MOBILE-REACT-NATIVE.md | **Token-Optimized**

## Component Patterns

### Component Structure
```typescript
// Base component template
import { View, Text, StyleSheet } from 'react-native';

interface ComponentNameProps {
  required: string;
  optional?: number;
  onAction?: () => void;
}

export function ComponentName({ required, optional, onAction }: ComponentNameProps) {
  return (
    <View style={styles.container}>
      <Text>{required}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
});
```

### Composition over Inheritance
```typescript
// ✅ GOOD - Compose smaller components
export function ItemCard({ item }: ItemCardProps) {
  return (
    <Card>
      <CardHeader title={item.title} />
      <CardBody>
        <PropertysList items={item.propertys} />
      </CardBody>
      <CardFooter>
        <Button title="View" onPress={() => {}} />
      </CardFooter>
    </Card>
  );
}

// ❌ BAD - Monolithic component
export function ItemCard({ item }: ItemCardProps) {
  return (
    <View>
      {/* 200 lines of JSX */}
    </View>
  );
}
```

### Reusable UI Components
```typescript
// components/ui/Card.tsx
export function Card({ children, style }: CardProps) {
  return <View style={[styles.card, style]}>{children}</View>;
}

// components/ui/Button.tsx
export function Button({ title, onPress, variant = 'primary', loading }: ButtonProps) {
  return (
    <Pressable
      style={[styles.button, styles[variant]]}
      onPress={onPress}
      disabled={loading}
    >
      {loading ? <ActivityIndicator /> : <Text>{title}</Text>}
    </Pressable>
  );
}

// components/ui/Input.tsx
export function Input({ value, onChangeText, placeholder, error }: InputProps) {
  return (
    <View>
      <TextInput
        style={[styles.input, error && styles.inputError]}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
      />
      {error && <Text style={styles.error}>{error}</Text>}
    </View>
  );
}
```

## Styling Patterns

### Design System Constants

**⚠️ IMPORTANT**: The values below are example patterns. For your actual project, use the values defined in `agent-os/product/design-system.md` (created during `/plan-product`).

```typescript
// constants/theme.ts
// 📖 Reference: Get actual values from agent-os/product/design-system.md
// This file shows HOW to structure the code, not WHAT values to use

export const COLORS = {
  primary: '#FF6B6B',      // ← Replace with your Primary color from design-system.md
  secondary: '#4ECDC4',    // ← Replace with your Secondary color
  success: '#51CF66',      // ← Replace with your Success color
  warning: '#FFD93D',      // ← Replace with your Warning color
  error: '#EF4444',        // ← Replace with your Error color

  text: {
    primary: '#1F2937',    // ← Replace with your Text Primary color
    secondary: '#6B7280',  // ← Replace with your Text Secondary color
    tertiary: '#9CA3AF',
  },

  background: {
    primary: '#FFFFFF',    // ← Replace with your Background color
    secondary: '#F9FAFB',  // ← Replace with your Background Secondary color
    tertiary: '#F3F4F6',
  },

  border: '#E5E7EB',       // ← Replace with your Border color
};

export const SPACING = {
  xs: 4,    // ← Use spacing values from design-system.md
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const TYPOGRAPHY = {
  h1: { fontSize: 32, fontWeight: '700', lineHeight: 40 },  // ← Use typography from design-system.md
  h2: { fontSize: 24, fontWeight: '600', lineHeight: 32 },
  h3: { fontSize: 20, fontWeight: '600', lineHeight: 28 },
  body: { fontSize: 16, fontWeight: '400', lineHeight: 24 },
  small: { fontSize: 14, fontWeight: '400', lineHeight: 20 },
  caption: { fontSize: 12, fontWeight: '400', lineHeight: 16 },
};

export const SHADOWS = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 2,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
};
```

**Workflow:**
1. During `/plan-product`: Define your brand colors/fonts in `design-system.md`
2. During `/implement-tasks`: Use this pattern to create `constants/theme.ts` with your actual values

### StyleSheet Patterns
```typescript
import { StyleSheet } from 'react-native';
import { COLORS, SPACING, TYPOGRAPHY } from '@/constants/theme';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background.primary,
    padding: SPACING.md,
  },

  // Use theme constants
  title: {
    ...TYPOGRAPHY.h2,
    color: COLORS.text.primary,
    marginBottom: SPACING.sm,
  },

  // Flexbox layouts
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: SPACING.sm,
  },

  // Responsive spacing
  card: {
    backgroundColor: COLORS.background.primary,
    borderRadius: 12,
    padding: SPACING.md,
    ...SHADOWS.md,
  },
});
```

### Responsive Design
```typescript
import { Dimensions, Platform } from 'react-native';

const { width, height } = Dimensions.get('window');

// Breakpoints
export const BREAKPOINTS = {
  sm: 380,
  md: 768,
  lg: 1024,
};

export const isSmallDevice = width < BREAKPOINTS.sm;
export const isTablet = width >= BREAKPOINTS.md;

// Responsive values
export function getFontSize(base: number): number {
  if (isSmallDevice) return base * 0.9;
  if (isTablet) return base * 1.1;
  return base;
}

// Usage in styles
const styles = StyleSheet.create({
  title: {
    fontSize: getFontSize(24),
  },

  container: {
    padding: isSmallDevice ? SPACING.sm : SPACING.md,
  },
});
```

## Accessibility

### Basic Accessibility
```typescript
// Always add accessibility labels
<Pressable
  accessibilityLabel="Delete item"
  accessibilityHint="Double tap to delete this item permanently"
  accessibilityRole="button"
  onPress={handleDelete}
>
  <Icon name="trash" />
</Pressable>

// Text alternatives for images
<Image
  source={{ uri: item.image }}
  accessibilityLabel={`Photo of ${item.title}`}
/>

// Form inputs
<TextInput
  accessibilityLabel="Email address"
  accessibilityHint="Enter your email to sign in"
  placeholder="email@example.com"
  autoComplete="email"
  keyboardType="email-address"
/>
```

### Screen Reader Support
```typescript
import { AccessibilityInfo } from 'react-native';

// Announce messages
AccessibilityInfo.announceForAccessibility('Item added successfully');

// Group related content
<View accessible accessibilityLabel="Item propertys">
  {propertys.map(ing => <Text key={ing}>{ing}</Text>)}
</View>

// Skip decorative elements
<View accessibilityElementsHidden>
  <Icon name="decorative-pattern" />
</View>
```

### Touch Targets
```typescript
// Minimum 44x44 points for touch targets
const styles = StyleSheet.create({
  button: {
    minHeight: 44,
    minWidth: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },

  // Increase touch area with hitSlop
  smallIcon: {
    width: 24,
    height: 24,
  },
});

<Pressable
  style={styles.smallIcon}
  hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
  onPress={handlePress}
>
  <Icon name="close" size={24} />
</Pressable>
```

## Performance Optimization

### React.memo for Pure Components
```typescript
import { memo } from 'react';

// Memoize components that don't need frequent re-renders
export const ItemCard = memo(({ item }: ItemCardProps) => {
  return (
    <Card>
      <Text>{item.title}</Text>
    </Card>
  );
});

// Custom comparison
export const ItemCard = memo(
  ({ item }: ItemCardProps) => { /* ... */ },
  (prevProps, nextProps) => prevProps.item.id === nextProps.item.id
);
```

### useMemo & useCallback
```typescript
import { useMemo, useCallback } from 'react';

function ItemList({ items, onSelectItem }: ItemListProps) {
  // Memoize expensive computations
  const sortedItems = useMemo(() => {
    return [...items].sort((a, b) => a.title.localeCompare(b.title));
  }, [items]);

  // Memoize callbacks to prevent child re-renders
  const handleSelect = useCallback((id: string) => {
    onSelectItem(id);
  }, [onSelectItem]);

  return (
    <FlatList
      data={sortedItems}
      renderItem={({ item }) => (
        <ItemCard item={item} onPress={() => handleSelect(item.id)} />
      )}
    />
  );
}
```

### FlatList Optimization
```typescript
<FlatList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={(item) => item.id}

  // Performance optimizations
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  updateCellsBatchingPeriod={50}
  initialNumToRender={10}
  windowSize={10}

  // Pull to refresh
  refreshing={isRefreshing}
  onRefresh={handleRefresh}

  // Infinite scroll
  onEndReached={loadMore}
  onEndReachedThreshold={0.5}
  ListFooterComponent={isLoading ? <LoadingSpinner /> : null}
/>
```

## Best Practices

1. **Components**: Small, focused, single responsibility
2. **Styling**: Use theme constants, StyleSheet.create, avoid inline styles
3. **Accessibility**: Always add labels, test with screen reader
4. **Performance**: Memo expensive components, FlatList for long lists
5. **Responsive**: Use relative values, test on multiple screen sizes
6. **Touch Targets**: Minimum 44x44 points
7. **Color Contrast**: WCAG AA minimum (4.5:1 for text)
8. **Forms**: Proper keyboard types, autoComplete, validation

---

**Token Count**: ~900 tokens | **Use with**: MOBILE-REACT-NATIVE.md
