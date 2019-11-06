> pip3 install numpy matplotlib opencv-python
```
usage: main.py [-h] [--verbose]
               input_image
               number_of_components
               [output_image]

Image compression through Principal Component Analysis.

positional arguments:
  input_image           Input image file name (with path)
  number_of_components  Number of principal components to be used
  output_image          Output compressed image file name (with path)

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         Increase verbosity
```
`for %x in (1, 5, 10, 50, 100, 150, 200, 250, 300, 400, 500, 512) do python main.py i\lenna.png %x`