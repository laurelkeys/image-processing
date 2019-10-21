## Install dependencies
> pip3 install numpy matplotlib opencv-python
## Example usage
`$ python3 encode.py input_image.png message_in.txt output_image.png [bit_plane]`  
`$ python3 decode.py output_image.png message_out.txt [bit_plane]`
## [encode.py](https://github.com/laurelkeys/image-processing/blob/master/assignment-4/encode.py)
```
usage: encode.py [-h]
                 --input_image INPUT_IMAGE
                 --message MESSAGE
                 --output_image OUTPUT_IMAGE
                 [--bit_plane {0,1,2,3,4,5,6,7}]

required arguments:
  --input_image INPUT_IMAGE, -i INPUT_IMAGE
                        Input image file name (with path), in which the
                        message will be embedded
  --message MESSAGE, -m MESSAGE
                        Text file name (with path), containing the message to
                        hide
  --output_image OUTPUT_IMAGE, -o OUTPUT_IMAGE
                        Output image file name (with path)
optional arguments:
  -h, --help            show this help message and exit
  --bit_plane {0,1,2,3,4,5,6,7}, -b {0,1,2,3,4,5,6,7}
                        Bit plane in which to hide the message (default: 0)
```
## [decode.py](https://github.com/laurelkeys/image-processing/blob/master/assignment-4/decode.py)
```
usage: decode.py [-h]
                 --image IMAGE
                 --message MESSAGE
                 [--bit_plane {0,1,2,3,4,5,6,7}]

required arguments:
  --image IMAGE, -i IMAGE
                        File name (with path) of the image in which the
                        message is embedded
  --message MESSAGE, -m MESSAGE
                        Text file name (with path) for which to save the
                        decoded message
optional arguments:
  -h, --help            show this help message and exit
  --bit_plane {0,1,2,3,4,5,6,7}, -b {0,1,2,3,4,5,6,7}
                        Bit plane in which the message is hidden (default: 0)
```