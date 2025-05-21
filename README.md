# Highlight Imprecise Italic Angle

A plugin for the [Glyphs font editor](http://glyphsapp.com/).

Highlights the path segments which angle is not precise to master's Italic Angle and is within observed angle range (±10 degrees around Italic Angle). Also it adds dots around the nodes to indicate the horizontal direction of node movement for angle correction.

![](PreviewAnimation.gif)

# Features

- Red color means that the segment most likely needs correction.
- Yellow color means that the segment angle is almost precise (±0.5 degree around Italic Angle) so you may decide to just leave it as is.

# Background

The issue of path correction after interpolation is always relevant, especially for italic styles. Usually the glyph shape has its own differences in different masters, so after interpolation (and more often after extrapolation) there are possible kinks, broken rounded nodes, and deviations from the Italic Angle. Read more about the issue on [Glyphs forum](https://forum.glyphsapp.com/t/is-there-a-quick-way-to-fix-paths-after-interpolation/3311). Usually, RMX Tools is used to correct such errors. On the other hand, *Highlight Imprecise Italic Angle* is more designed for manual review of each glyph, because sometimes it should be estimated by eye and the correction is not always needed.

# To Do

I am considering the possibility of some automation in the future. So far, I see this as a separate script or set of scripts (with shortcuts) in addition to this plugin, which can be applied after visually deciding what exactly needs to be corrected and whether it will do more harm than good. Need more real testing experience for this.