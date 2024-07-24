# Python Interface Package for Nanonis 

Official python package for the Nanonis TRAMEA Controller software.

## Usage

This package allows users of the Nanonis TRAMEA Controller software to use and control
said software through python commands.

## How to use

### Importing

import nanonis_tramea

### Initializing Connection

nanonisInstance = nanonis_tramea.Nanonis(6501, '10.10.10.10')

NOTE : THE PORT HAS TO BE AN INTEGER AND THE IP ADRESS A STRING

### Example

nanonisInstance.BiasSpectr_Open() --> Opens Bias Spectroscopy Module.

Funtion Documentations can be found by either hovering over the function names
or in the TCP Protocol Document, which is also where all the available functions
are listed.




