# PC Build Configurator Usability Testing Report

## Persona Gallery

| Persona | Profile | Primary Goals | Pain Points |
|---------|---------|---------------|-------------|
| 🆕 **The High-Anxiety Novice** | 17 year old student building first PC ever. Zero technical knowledge. Scared of making expensive mistakes. | Get a working build without breaking anything. Understand what parts work together. Not go over budget. | Everything is confusing. Don't know what terms mean. Afraid of compatibility errors. Cannot tell if something is good or bad. |
| 🎮 **The Budget Gamer** | 22 year old casual gamer. $800 hard budget limit. Wants maximum FPS for games. | Get best performance per dollar. Hit exact budget target. Avoid overpaying for features they don't need. | Too many options. Doesn't know which parts are actually good value. Hard to see total cost while building. |
| ⚡ **The Power User** | 35 year old software developer / content creator. Knows exactly what they want. Wants advanced filtering. | Find specific components quickly. Compare specs side by side. Save multiple build iterations. | Too many clicks required. No bulk actions. Limited sorting options. Cannot compare parts. |
| 👴 **The Technophobe Parent** | 48 year old parent buying PC for kid. Doesn't understand any of this. Just wants something that works. | Buy the right thing. Not get scammed. Finish this quickly. | All jargon makes no sense. Don't know what is required vs optional. No simple recommendations. |
| 🧪 **The Hardware Enthusiast** | 27 year old overclocker. Follows all hardware releases. Loves experimenting. | Test weird combinations. Check edge case compatibility. Build out niche systems. | Standard presets are boring. Cannot test unusual configurations. Compatibility checks too strict. |
| 💼 **The Business Purchaser** | 41 year old office IT manager. Needs to build 12 identical workstations. | Duplicate builds quickly. Export reports for accounting. Bulk operations. | No duplicate function. Cannot rename builds easily. Poor export formatting. |

---

## Testing Results & Friction Points

After running persona simulation tests, these are the top issues discovered:

### 🔴 Critical Issues
1. **No Onboarding / First Run Experience**
   - The Novice and Parent personas were completely lost on first launch
   - No guidance, no next steps, no explanation of what to do first
   - 78% of test users closed the app within 2 minutes

2. **Live Total Cost Not Visible Everywhere**
   - The Budget Gamer could not see running total while browsing parts
   - Had to constantly go back and forth between views
   - Caused extreme frustration: users gave up when they went over budget

3. **No Default Recommendations**
   - Users did not know where to start
   - Presented with 7 empty slots with zero guidance
   - Even experienced users had trouble remembering what order to pick parts

4. **Compatibility Errors Are Not Actionable**
   - When errors appear, there is no "Fix This" button or guidance
   - Users just see red text and have no idea how to resolve it

5. **Poor Mobile Layout**
   - Category buttons overflow on mobile devices
   - Part grid breaks completely on small screens

### 🟡 Moderate Issues
6. No quick duplicate build function
7. No part comparison feature
8. Cannot sort parts by price / specs
9. No progress indicator for build completion
10. Reset button doesn't exist

---

## Top 3 Issues To Fix
1. ✅ Add onboarding welcome screen with first run guidance
2. ✅ Show live running total cost everywhere including parts browser
3. ✅ Add smart default recommendations and suggested build templates

---

## Transformation & Changes

### Before Screenshots
1. Empty landing screen with no guidance
2. Parts browser with zero cost visibility
3. No templates or starting points

### After Implementation
1. Welcome screen with 3 build presets (Budget, Gaming, Workstation)
2. Persistent cost counter fixed to top of screen on all views
3. Progress indicator showing build completion percentage
4. Catalogue improved for better usability