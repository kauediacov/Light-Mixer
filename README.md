# Light Controller Addon for Blender

## Authors
- Higor Pereira
- Kaue Diacov
- Vitoria Ferreira

## Overview
Light Controller is a Blender addon that provides a comprehensive interface for managing all lights in your scene from a single panel. It simplifies the process of adjusting multiple lights and offers advanced features for light management.

## Features

### 1. Centralized Light Management
- View and control all scene lights from a single panel
- Real-time light parameter adjustments
- Quick access to common light properties

### 2. Light Properties Control
- Power/Energy adjustment
- Color control
- Spread control (specific to each light type)
- Shadow settings
  - Toggle shadows
  - Shadow softness
  - Shadow bias
- Node-based material support

### 3. Light Organization
- Collection-based filtering (up to 5 collections)
- Isolation features:
  - Isolate individual lights
  - Isolate lights by collection
- Quick visibility toggles
  - Viewport visibility
  - Render visibility

### 4. Selection and Navigation
- Quick light selection in viewport
- Direct access to node editor
- Rename lights directly from the panel

## Installation
1. Download the addon file
2. In Blender, go to Edit > Preferences > Add-ons
3. Click "Install" and select the downloaded file
4. Enable the addon by checking the checkbox

## Location
Access the addon from: View3D > Sidebar > Light Controller

## Panel Sections

### All Lights Panel
- Shows a comprehensive list of all lights in the scene
- Each light has its own control box with:
  - Selection button
  - Visibility toggles
  - Name field
  - Isolation toggle
  - Power control
  - Color picker
  - Type-specific spread control
  - Shadow settings
  - Node editor access

### Collections Panel
- Manage lights by collections
- Add up to 5 collection filters
- Isolate lights by collection
- Quick access to lights within each collection

## Usage Tips

### Light Isolation
- Use the solo icon to isolate individual lights
- Use collection isolation to focus on lights in specific collections
- Click "Show All Lights" to reset isolation

### Collection Management
- Add collections using the + button
- Remove collections using the X button
- Toggle collection isolation using the solo icon

### Node Editor Access
1. Enable nodes for a light
2. Click the editor button to open the node editor
3. The system will automatically switch to the light's node tree

## Requirements
- Blender 3.0.0 or newer

## Known Limitations
- Maximum of 5 collection filters
- Node editor will split the largest area when no node editor is present

## Support
For issues, questions, or suggestions, please contact the authors:
- Higor Pereira
- Kaue Diacov
- Vitoria Ferreira 