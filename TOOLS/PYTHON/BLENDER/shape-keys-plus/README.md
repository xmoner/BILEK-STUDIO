### **Welcome to the documentation about Shape Keys Plus**
...for duplicating and mirroring shape keys (in Maya software called Blendshapes ("BS") )

### About:

Author: Lukas Bilek. BILEK STUDIO.

Date created: 6 Jun 2021

Copyright: GPL

Contact: https://www.linkedin.com/in/lukasbilek/

How to support me: On Blender market: www.blendermarket.com or contact me on linked it and say something nice. :-)
    
This tools is suppose to make easier life for artist who is working with shape keys (BS).
You should find the buttons under Shape Keys Special in Shape Keys attributes.

### List of buttons:

"Duplicate & mirror from L_ > R_"

"Duplicate & mirror from R_ > L_"

"Duplicate & mirror all L_ >> R_"

"Duplicate & mirror all R_ >> L_"

"Shape Keys Plus HELP'

### What it is doing:
- Before clicking on any buttons, you have to select one or more objects in the scene to get it work.
    - "Duplicate & mirror from L_ >> R_" is duplicating and mirroring selected shape key from L_ to R_side
       This means that it will take "L_" (l_) prefix or "_L" (l_) suffix and rename them to R after duplicating and mirroring shape keys.
       Also it is removing R_ shape keys if exist with the same name as from selected L side, just it replacing L to R 
       in the search and then remove it.
    - "Duplicate & mirror from R_ >> L_" is similar to the "Duplicate & mirror from L_ >> R_" just it works via versa.
    - "Duplicate & mirror all L_ >> R_" is removing all existing right shapes which have R preffix or suffix,
      then it duplicate each left side, mirror them and rename to R side as well.
    - "Duplicate & mirror all R_ >> L_" is same as "Duplicate & mirror all L_ >> R_" just from Right to Left sides.
    
**_What information should the tool copy when clicked on the buttons:_**

- ##**In version 0.2.0:**
    - Duplicating shape keys.
    - Mirroring shape keys after duplicating.
    - Renaming Shape Keys such as [L_] [l_] [_L] [_l] (prefix and suffix) [R_] [r_] [_R] [_r]) 
    - Removing shape keys if needs to be removed for creating new shape keys.
    - Expressions - it copies some expressions, but not recommended.
    - Copying an attribute from Range Min in Shape Keys.
    - Copying an attribute from Range Max in Shape Keys.
    - Able to generate Shape keys with multiply / more objects.
