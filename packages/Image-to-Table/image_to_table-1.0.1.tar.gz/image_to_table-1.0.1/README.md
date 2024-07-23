# Image-to-table

Utilize a MultiModal Large Language Modal `GEMINI` to extract `table data` from an `image` and saves it as a `json`

## Installing

Install from PyPi using

```bash
python -m pip install randomgen
```

## Documentation

To generate the table and save it as json:

```bash
from image_to_table import generate_timetable

generate_timetable('output.json','API_KEY')
```

the input image should be placed in images directory

To visualize the json output:

```bash
from image_to_table import json_to_table

json_to_table('output.json')
```

this function prints the output to the console like the test below

## Testing

Test with timetable:

![test](https://github.com/user-attachments/assets/927f399b-2bd1-4e43-9096-b26ed4e7bed5)

Output:
![2024-07-1615-51-24-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/38f36dc3-1f9c-4482-86f2-5f6b2867fec1)
