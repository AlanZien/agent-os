# shadcn/ui + Tailwind CSS Standards

> **Sources:**
> - [shadcn/ui Documentation](https://ui.shadcn.com)
> - [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## Overview

Standards pour l'utilisation de shadcn/ui et Tailwind CSS dans AgentOS Tracker. shadcn/ui n'est pas une bibliothèque de composants traditionnelle - c'est une collection de composants copiés dans votre projet que vous pouvez modifier librement.

## Philosophie shadcn/ui

1. **Open Code** - Le code des composants est dans votre projet, pas dans node_modules
2. **Composition** - Interface composable commune à tous les composants
3. **Distribution** - Schéma et CLI pour partager des composants
4. **Beautiful Defaults** - Styles par défaut soignés, facilement personnalisables
5. **AI-Ready** - Structure lisible par les LLMs pour génération de code

## Installation de Composants

```bash
# Installation via CLI
npx shadcn@latest add button
npx shadcn@latest add form
npx shadcn@latest add input

# Installation multiple
npx shadcn@latest add button card form input label
```

Les composants sont installés dans `components/ui/`.

## Structure des Fichiers

```
components/
├── ui/                          # shadcn/ui components (auto-generated)
│   ├── button.tsx
│   ├── card.tsx
│   ├── form.tsx
│   ├── input.tsx
│   └── label.tsx
├── features/                    # Feature-specific components
│   └── auth/
│       ├── LoginForm.tsx        # Uses ui/ components
│       └── SignupForm.tsx
└── providers/
    └── ThemeProvider.tsx
```

## Tailwind Configuration

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['class'],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // AgentOS Tracker Design System
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',       // #10B981 (teal)
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',   // #EF4444 (red)
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}
export default config
```

## CSS Variables (Dark Theme)

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* AgentOS Tracker Dark Theme */
    --background: 0 0% 5%;            /* #0D0D0D */
    --foreground: 0 0% 98%;

    --card: 0 0% 9%;                  /* #171717 */
    --card-foreground: 0 0% 98%;

    --primary: 160 84% 39%;           /* #10B981 (teal) */
    --primary-foreground: 0 0% 98%;

    --secondary: 0 0% 14%;            /* #242424 */
    --secondary-foreground: 0 0% 98%;

    --muted: 0 0% 14%;
    --muted-foreground: 0 0% 64%;     /* #A3A3A3 */

    --destructive: 0 84% 60%;         /* #EF4444 */
    --destructive-foreground: 0 0% 98%;

    --border: 0 0% 18%;               /* #2E2E2E */
    --input: 0 0% 18%;
    --ring: 160 84% 39%;              /* Focus ring = primary */

    --radius: 0.5rem;                 /* 8px */
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

## Patterns de Composants

### Button Variants

```tsx
import { Button } from '@/components/ui/button'

// Primary (teal)
<Button>Sign In</Button>

// Destructive (red)
<Button variant="destructive">Delete</Button>

// Outline
<Button variant="outline">Cancel</Button>

// Ghost (no background)
<Button variant="ghost">Learn more</Button>

// Loading state
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Please wait
</Button>
```

### Form avec Validation (React Hook Form + Zod)

```tsx
'use client'

import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'

const formSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

type FormValues = z.infer<typeof formSchema>

export function LoginForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  })

  async function onSubmit(values: FormValues) {
    // Handle submission
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="email@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type="password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">
          Sign In
        </Button>
      </form>
    </Form>
  )
}
```

### Card Layout

```tsx
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

<Card className="w-full max-w-md">
  <CardHeader>
    <CardTitle>Sign In</CardTitle>
    <CardDescription>
      Enter your credentials to access your account
    </CardDescription>
  </CardHeader>
  <CardContent>
    <LoginForm />
  </CardContent>
  <CardFooter className="flex justify-center">
    <p className="text-sm text-muted-foreground">
      Don't have an account?{' '}
      <Link href="/signup" className="text-primary hover:underline">
        Sign up
      </Link>
    </p>
  </CardFooter>
</Card>
```

### Loading Skeleton

```tsx
import { Skeleton } from '@/components/ui/skeleton'

// Card skeleton
<div className="space-y-4">
  <Skeleton className="h-8 w-48" />
  <Skeleton className="h-4 w-full" />
  <Skeleton className="h-4 w-3/4" />
</div>

// Avatar skeleton
<Skeleton className="h-12 w-12 rounded-full" />

// Form skeleton
<div className="space-y-4">
  <Skeleton className="h-10 w-full" />
  <Skeleton className="h-10 w-full" />
  <Skeleton className="h-10 w-32" />
</div>
```

## Design System - AgentOS Tracker

### Spacing

```tsx
// Standard spacing scale
className="p-4"     // 16px - Default padding
className="p-6"     // 24px - Card padding
className="p-8"     // 32px - Large section padding
className="space-y-4"  // 16px vertical gap
className="gap-4"   // 16px grid/flex gap
```

### Typography

```tsx
// Headings
className="text-2xl font-bold"          // Page titles
className="text-lg font-semibold"       // Section titles
className="text-base"                   // Body text
className="text-sm text-muted-foreground"  // Secondary text
className="text-xs"                     // Labels, captions

// Colors
className="text-foreground"             // Primary text
className="text-muted-foreground"       // Secondary text (#A3A3A3)
className="text-primary"                // Accent text (#10B981)
className="text-destructive"            // Error text (#EF4444)
```

### Form Elements

```tsx
// Input styling (already handled by shadcn)
// Height: 40px, Border radius: 6px
<Input className="h-10" />

// Custom input with icon
<div className="relative">
  <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
  <Input className="pl-10" placeholder="Email" />
</div>

// Error state
<Input className="border-destructive" />
<p className="text-sm text-destructive">Error message</p>
```

### Button Sizes

```tsx
// Full width (forms)
<Button className="w-full">Submit</Button>

// Standard
<Button>Action</Button>

// Small
<Button size="sm">Small</Button>

// Icon button
<Button size="icon">
  <Plus className="h-4 w-4" />
</Button>
```

## Responsive Design

```tsx
// Mobile-first breakpoints
className="p-4 md:p-6 lg:p-8"
className="text-sm md:text-base"
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"

// Hide/show at breakpoints
className="hidden md:block"    // Hidden on mobile
className="block md:hidden"    // Visible only on mobile
```

## Animation Utilities

```tsx
// Tailwind animate plugin
className="animate-spin"       // Loading spinners
className="animate-pulse"      // Skeleton loading
className="animate-bounce"     // Attention

// Transitions
className="transition-colors"  // Color transitions
className="transition-all duration-200"  // Smooth transitions

// Hover states
className="hover:bg-primary/90"
className="hover:text-primary"
```

## Customisation des Composants

Modifier directement le fichier dans `components/ui/`:

```tsx
// components/ui/button.tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center...",
  {
    variants: {
      variant: {
        // Add custom variant
        success: "bg-green-500 text-white hover:bg-green-600",
      },
    },
  }
)
```

## Best Practices

1. **Utiliser les CSS variables** pour la cohérence du thème
2. **Composer les composants** plutôt que de les modifier excessivement
3. **Mobile-first** - Commencer par les styles mobiles
4. **Consistent spacing** - Utiliser l'échelle de spacing Tailwind
5. **Semantic classes** - `text-muted-foreground` plutôt que `text-gray-500`
6. **Accessible by default** - Les composants shadcn incluent l'a11y
