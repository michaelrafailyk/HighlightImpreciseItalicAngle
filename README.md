# Highlight Imprecise Italic Angle

A plugin for the [Glyphs font editor](http://glyphsapp.com/).

Highlights the path segments which angle is not precise (or not closest) to Italic Angle of the selected master and is within observed angle range (±10 degrees around Italic Angle). Also it adds placeholder dots around the nodes to indicate the horizontal direction and position for better node placement where segment's angle will be precise to Italic Angle (or smaller of it if precise angle isn't available).

![](PreviewAnimation.gif)

# Italic Angle

The Italic Angle is taken from Font Info -> Masters. If you work with italic master, the plugin will check the vertical segments and handles around Italic Angle. Also, it is worth noting that even upright styles have Italic Angle parameter set to 0. And if you work with upright master, the plugin will check all the vertical stems and handles that are not precise to 0 degree.

# Rounding

If the precise angle is not possible to fit because of grid rounding and integer coordinates, In this case the smaller (from italic) angle will be chosen.

# Distance

The distance from a node to the placeholder dot is displayed in number next to the placeholder dot, so it is easier to know how much the node should be moved to fit the correct position. For example, if you see the number 4, you need to press the left or right arrow key 4 times. It makes the correction faster.

# Background

The issue of path correction after interpolation is always relevant, especially for italic styles. Usually the glyph shape has its own differences in different masters, so after interpolation (and more often after extrapolation) there are possible kinks, broken rounded nodes, and deviations from the Italic Angle. Read more about the issue in topic [Is there a quick way to fix paths after interpolation?](https://forum.glyphsapp.com/t/is-there-a-quick-way-to-fix-paths-after-interpolation/3311). Usually, RMX Tools is used to correct such errors. On the other hand, *Highlight Imprecise Italic Angle* is more designed for manual review of each glyph, because sometimes it should be estimated by eye and the correction is not always needed.
