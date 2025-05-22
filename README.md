# Highlight Imprecise Italic Angle

A plugin for the [Glyphs font editor](http://glyphsapp.com/).

Highlights the path segments which angle is not precise to Italic Angle of the selected master and is within observed angle range (±10 degrees around Italic Angle). Also it adds placeholder dots around the nodes to indicate the horizontal direction and position for better node placement where segment will fit Italic Angle.

![](PreviewAnimation.gif)

# Colors

- Red color means that the segment most likely needs correction.
- Yellow color means that the segment angle is almost precise (±0.5 degree around Italic Angle) so you may decide to just leave it as is.

# Angles

The angle is taken from Font Info -> Masters. That is, the plugin check only the vertical segments. If you work with italic master, it will be whatever 8-12 the master use for Italic Angle. If you work with upright master, the plugin will check all the vertical stems and handles at 0 degree.

# Distance

The distance from a node to the placeholder dot is displayed in number next to the placeholder dot, so it is easier to know how much the node should be moved to fit the correct position. For example, if you see the number 4, you need to press the left or right arrow key 4 times. It makes the correction faster.

# Background

The issue of path correction after interpolation is always relevant, especially for italic styles. Usually the glyph shape has its own differences in different masters, so after interpolation (and more often after extrapolation) there are possible kinks, broken rounded nodes, and deviations from the Italic Angle. Read more about the issue in topic [Is there a quick way to fix paths after interpolation?](https://forum.glyphsapp.com/t/is-there-a-quick-way-to-fix-paths-after-interpolation/3311). Usually, RMX Tools is used to correct such errors. On the other hand, *Highlight Imprecise Italic Angle* is more designed for manual review of each glyph, because sometimes it should be estimated by eye and the correction is not always needed.

# To Do

I am considering the possibility of some automation in the future. So far, I see this as a separate script or set of scripts (with shortcuts) in addition to this plugin, which can be applied after visually deciding what exactly needs to be corrected and whether it will do more harm than good. I think, automatically aligning two handles around a smooth node will be an easy task. Need more real testing experience for this.