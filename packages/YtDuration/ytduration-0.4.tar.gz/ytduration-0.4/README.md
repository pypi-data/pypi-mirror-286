# YT Duration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This Python package retrieves the duration of a YouTube video without using the YouTube Data API.

### Explanation:
The `YtDuration` package provides a function to extract the duration of a YouTube video from its URL by web scraping the video's page and parsing the duration information.

## Installation

To install the package, use the following command:

```bash
pip install YtDuration
```

### Usage
Here is an example of how to use the package:

```python
import yt_duration import YtDuration as yt
video_url = 'YouTube_url'
duration = yt(video_url)
print("Video Duration:", duration)
```
### Thank You
Thank you for using YtDuration. We hope you find it helpful. If you have any questions or feedback, please don't hesitate to reach out!