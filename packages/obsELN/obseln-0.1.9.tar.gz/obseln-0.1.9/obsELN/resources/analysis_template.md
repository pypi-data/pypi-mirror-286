---
# Obsidian ELN, version: 0.3.2
# author: Dr. Frieder Scheiba, mail: frieder.scheiba@kit.edu
# copyright: GNU Affero General Public License v3.0
#
ELN info:
   template: Analysis Template (Python)
   version: eln-version
   author: Frieder Scheiba
   copyright: GNU Affero General Public License v3.0
# Layout / Styling
cssclass: analysis-note
# Navigation
parent: "[[sample-note]]"
# Note Information
author: Name Surname
date created: 2023-08-02
note type: analysis
tag:
  - " #analysis "
# ELN Meta Data
project:
   name: project-name
   link: "[[project-name]]"
sample:
   name: sample-name
   type: sample-type
   description: sample-description
instrument:
   name: instrument-name
   link: "[[instrument-name]]"
   type: instrument-type
session:
   part of session: false
   name: none
   number of analyses: 0
analysis:
   method: analysis-method
   # Analysis Meta Data
   date: analysis-date
   time: analysis-time
   operator: analysis-operator
   status: completed
   parameters: 
   data:
      local:
         file: local-data-file
         folder: local-data-folder
         link: "[local data file](link-to-local-data-file)"
         folder_link: "[local data folder](link-to-local-data-folder)"
      remote:
         file: remote-data-file
         folder: remote-data-folder
         link: "[remote data file](link-to-remote-data-file)"
         folder_link: "[remote data folder](link-to-remote-data-folder)"
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/properties", {key: "sample"});
```

## Data Preview

<* data_preview *>

## My Notes

> [!Info] Create your custom template section that will be added to your Analysis Notes.
> Open [[Custom Analysis Template]] to modify it.


```dataviewjs
await dv.view("/assets/javascript/dataview/views/properties", {});
```

<* settings_view *>

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
