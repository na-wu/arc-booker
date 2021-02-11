## Quick Start
- `git clone https://github.com/na-wu/arc-booker.git`
- `cd arc-booker`
- `cp credentials.example.py credentials.py`
- Add your CWL
- Download latest Chrome driver @ https://chromedriver.chromium.org/downloads
- Place `chromedriver.exe` in `arc-booker/`
- `pip install selenium`
- `python Book.py --slot [N]` where N is the time slot from [1-9] on weekdays and [1-6] on weekends