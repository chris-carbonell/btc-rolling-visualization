# BTC Rolling Visualization

<b>BTC Rolling Visualization</b> creates the nearly eight thousand graphs behind the rolling visualization of BTC price over time.

# GIF (Trimmed)

![BTC Price](https://github.com/chris-carbonell/btc_rolling_visualization/blob/0c6023579d865b5c7acde099e4f5406c369f166e/output/btc.gif)

*Note.* The GIF is compressed from a 100 MB MP4.

# Quickstart

After installing the required dependencies, to build the graphs, simply run:<br>
<code>python -m build_plots</code>

# Requirements

* Python 3.9.0 (mostly, matplotlib/seaborn and pandas)
* ffmpeg
* video editor (e.g., OpenShot Video Editor)

# Process

1. Build plots via Python (<code>build_plots.py</code>)
2. Combine .png files to video using ffmpeg (<code>./ffmpeg/create_videos.bat</code>)
3. (Optional) Combine the videos in a video editor for final touches

# Resources
* ffmpeg Documentation<br>
https://ffmpeg.org/ffmpeg.html
* OpenShot Video Editor<br>
https://www.openshot.org/
