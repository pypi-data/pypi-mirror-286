# Floryn

Floryn is a package to create a visualization plot where the text is filled up to certain percentage.
This is used to emphasize the value, for example by comparing the before and after a product launch, in terms of percentage, compared to a target value.

## How to install
simply run
`pip install floryn`

## How to run
```python
import floryn

floryn.pp('Halo halo Bandung', percentage=0.5, color='denim blue', ax=None)
```

and this the example output
![Output](output.png "Result")

See example notebook for more plotting option, including different orientation, and even how to create an animation
