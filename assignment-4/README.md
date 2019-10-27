## Install dependencies
> pip3 install numpy matplotlib opencv-python
## Example usage
`$ python3 encode.py input_image.png message_in.txt bit_plane output_image.png`  
`$ python3 decode.py output_image.png bit_plane message_out.txt`
## [encode.py](https://github.com/laurelkeys/image-processing/blob/master/assignment-4/encode.py)
```
usage: encode.py [-h] [--verbose] [--very_verbose]
                 input_image message {0,1,2,3,4,5,6,7} output_image

Steganography algorithm to hide a text message in an image.

positional arguments:
  input_image          Input image file name (with path), in which the message
                       will be embedded
  message              Text file name (with path), containing the message to
                       hide
  {0,1,2,3,4,5,6,7}    Bit plane in which to hide the message
  output_image         Output image file name (with path)

optional arguments:
  -h, --help           show this help message and exit
  --verbose, -v        Increase verbosity
  --very_verbose, -vv  Increase verbosity even more (only recommended for
                       small input images)
```
## [decode.py](https://github.com/laurelkeys/image-processing/blob/master/assignment-4/decode.py)
```
usage: decode.py [-h] [--verbose] [--very_verbose]
                 image {0,1,2,3,4,5,6,7} message

Steganography algorithm to recover a text message hidden in an image.

positional arguments:
  image                File name (with path) of the image in which the message
                       is embedded
  {0,1,2,3,4,5,6,7}    Bit plane in which the message is hidden
  message              Text file name (with path) to which the decoded message
                       will be saved

optional arguments:
  -h, --help           show this help message and exit
  --verbose, -v        Increase verbosity
  --very_verbose, -vv  Increase verbosity even more (only recommended for
                       small input images)
```