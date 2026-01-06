# Design System - AgentOS Tracker

## Theme

**Dark theme** inspired by Claude Code / Auto Claude aesthetic - professional, developer-focused, modern.

## Palette de Couleurs

### Couleurs Primaires
- **Primary**: `#10B981` - Teal/emerald green, main brand color
- **Primary Dark**: `#059669` - Hover states, emphasis
- **Primary Light**: `#34D399` - Highlights, accents
- **Primary Muted**: `rgba(16, 185, 129, 0.1)` - Subtle backgrounds

### Couleurs de Surface (Dark Theme)
- **Background**: `#0D0D0D` - Main app background (near black)
- **Surface**: `#171717` - Cards, panels, elevated surfaces
- **Surface Elevated**: `#262626` - Modals, dropdowns, popovers
- **Border**: `#2E2E2E` - Subtle borders between elements
- **Border Strong**: `#404040` - Emphasized borders, dividers

### Couleurs de Texte
- **Text Primary**: `#FAFAFA` - Main text, headings
- **Text Secondary**: `#A3A3A3` - Secondary text, labels
- **Text Muted**: `#737373` - Placeholder text, disabled
- **Text Inverse**: `#0D0D0D` - Text on light/primary backgrounds

### Couleurs d'Etat
- **Success**: `#22C55E` - Completed, passed, positive
- **Error**: `#EF4444` - Errors, failed, destructive
- **Warning**: `#F59E0B` - Warnings, attention needed
- **Info**: `#3B82F6` - Information, links

### Couleurs de Statut (Kanban)
- **A Faire**: `#6B7280` - Gray, neutral pending state
- **En cours**: `#3B82F6` - Blue, active work
- **En attente**: `#F59E0B` - Amber, blocked/waiting
- **En cours de validation**: `#8B5CF6` - Purple, in review
- **Termine**: `#10B981` - Green, completed

### Couleurs de Priorite
- **Critical**: `#EF4444` - Red, urgent
- **High**: `#F97316` - Orange, important
- **Medium**: `#F59E0B` - Amber, normal
- **Low**: `#6B7280` - Gray, can wait

## Typographie

### Polices
- **Heading**: `Inter` - Clean sans-serif for headings (Google Fonts)
- **Body**: `Inter` - Consistent throughout the app
- **Monospace**: `JetBrains Mono` - Code snippets, IDs, technical text

### Tailles de Police
- **H1**: 30px / 700 / line-height: 1.2
- **H2**: 24px / 600 / line-height: 1.3
- **H3**: 20px / 600 / line-height: 1.4
- **H4**: 16px / 600 / line-height: 1.4
- **Body**: 14px / 400 / line-height: 1.5
- **Body Large**: 16px / 400 / line-height: 1.5
- **Small**: 13px / 400 / line-height: 1.4
- **Tiny**: 11px / 500 / line-height: 1.3 (labels, badges)

### Poids de Police
- **Bold**: 700 - H1, emphasis
- **Semibold**: 600 - H2-H4, buttons, labels
- **Medium**: 500 - Subtle emphasis
- **Regular**: 400 - Body text

## Spacing et Layout

### Systeme de Spacing (base 4px)
- **xs**: 4px (0.25rem)
- **sm**: 8px (0.5rem)
- **md**: 16px (1rem)
- **lg**: 24px (1.5rem)
- **xl**: 32px (2rem)
- **2xl**: 48px (3rem)
- **3xl**: 64px (4rem)

### Container
- **Max Width**: 1400px
- **Padding**: 16px (mobile) / 24px (tablet) / 32px (desktop)

### Sidebar
- **Width Collapsed**: 64px
- **Width Expanded**: 240px

### Border Radius
- **xs**: 4px - Small badges, tags
- **sm**: 6px - Inputs, small buttons
- **md**: 8px - Cards, buttons
- **lg**: 12px - Modals, larger cards
- **xl**: 16px - Feature sections
- **full**: 9999px - Pills, avatars

## Shadows (Dark Theme)

Dark themes use subtle shadows with lower opacity:

- **Small**: `0 1px 2px rgba(0, 0, 0, 0.3)` - Subtle lift
- **Medium**: `0 4px 6px rgba(0, 0, 0, 0.4)` - Cards, buttons
- **Large**: `0 10px 20px rgba(0, 0, 0, 0.5)` - Modals, dropdowns
- **Glow**: `0 0 20px rgba(16, 185, 129, 0.15)` - Primary element emphasis

## Composants Globaux

### Buttons

**Primary Button**
- Background: `#10B981`
- Text: `#0D0D0D`
- Height: 40px
- Padding: 16px horizontal
- Border Radius: 8px
- Font: 14px / 600
- Hover: `#059669`

**Secondary Button**
- Background: `transparent`
- Border: 1px solid `#404040`
- Text: `#FAFAFA`
- Hover Background: `#262626`

**Ghost Button**
- Background: `transparent`
- Text: `#A3A3A3`
- Hover Text: `#FAFAFA`
- Hover Background: `rgba(255, 255, 255, 0.05)`

**Destructive Button**
- Background: `#EF4444`
- Text: `#FAFAFA`
- Hover: `#DC2626`

### Inputs

- Height: 40px
- Background: `#171717`
- Border: 1px solid `#2E2E2E`
- Border Radius: 6px
- Padding: 12px horizontal
- Text: `#FAFAFA`
- Placeholder: `#737373`
- Focus Border: `#10B981`
- Focus Ring: `0 0 0 2px rgba(16, 185, 129, 0.2)`

### Cards

- Background: `#171717`
- Border: 1px solid `#2E2E2E`
- Border Radius: 8px
- Padding: 16px
- Shadow: Medium

### Badges/Tags

- Height: 24px
- Padding: 8px horizontal
- Border Radius: 4px
- Font: 11px / 500
- Background: varies by type (status/priority colors at 15% opacity)
- Text: corresponding status/priority color

### Kanban Cards

- Background: `#171717`
- Border: 1px solid `#2E2E2E`
- Border Radius: 8px
- Padding: 12px
- Shadow: Small
- Hover Border: `#404040`
- Dragging Shadow: Large + primary glow

### Modals

- Background: `#171717`
- Border: 1px solid `#2E2E2E`
- Border Radius: 12px
- Shadow: Large
- Overlay: `rgba(0, 0, 0, 0.8)`

### Sidebar

- Background: `#0D0D0D`
- Border Right: 1px solid `#2E2E2E`
- Active Item Background: `rgba(16, 185, 129, 0.1)`
- Active Item Border Left: 2px solid `#10B981`
- Hover Background: `rgba(255, 255, 255, 0.05)`

## Animations

### Transitions
- **Fast**: 100ms - Hover states, small interactions
- **Normal**: 200ms - Most transitions
- **Slow**: 300ms - Page transitions, modals

### Easing
- **Default**: `cubic-bezier(0.4, 0, 0.2, 1)` - Smooth, natural
- **In**: `cubic-bezier(0.4, 0, 1, 1)` - Acceleration
- **Out**: `cubic-bezier(0, 0, 0.2, 1)` - Deceleration

## Icons

- **Library**: Lucide React
- **Size Default**: 20px
- **Size Small**: 16px
- **Size Large**: 24px
- **Stroke Width**: 2px

## Style Notes

The design follows a **developer-tool aesthetic** similar to Claude Code:
- Dark, low-contrast backgrounds to reduce eye strain
- Teal/emerald accent color for a modern, fresh feel
- Generous spacing for clarity
- Clear visual hierarchy through color and weight
- Subtle borders rather than heavy shadows
- Status colors that are distinct but not overwhelming
- Monospace font for technical elements (IDs, dates, code)

Focus on **functionality over decoration** - every visual element should serve a purpose.
