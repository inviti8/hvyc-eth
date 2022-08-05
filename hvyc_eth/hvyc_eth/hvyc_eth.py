"""Heavy Meta HVYC Ethereum Contract Handler."""
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from jinja2 import Environment, FileSystemLoader
import json
import os

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
BURNABLE_IMPORT = 'import "@openzeppelin/contracts@4.7.2/token/ERC721/extensions/ERC721Burnable.sol"'
BURNABLE_TAG = 'ERC721Burnable,'
UINT_256 = 'uint256 '
UINT_MINT = 'uint256 {{intProp}} = (((randArr[0] % 100000000) / 1000000) % 18);'

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

#Begin Contract Data Classes-----------------------------

@dataclass_json
@dataclass      
class hvyc_data:
    name: str
    burnable_import: str
    burnable_tag: str
    price: str
    premium_price: str
    max_supply: str
    int_props: []
    int_mint_props: []
    int_params: str
    int_push: []
    int_method_props: []

#Begin Contract Data Classes-----------------------------

def HVYC_Burnable(name, price, prem_price, max_supply, prop_arr, meta_arr):
    '''
    Creates a burnable HVYC ERC721 contract from template based on passed
    parameters.
    :param name: string of the minter contract name
    :type name:  (str)
    :param price:  Price for NFT with randomly generated number properties.
    :type price: (str)
    :param prem_price:  Price for NFT that user can set number properties.
    :type prem_price: (str)
    :param max_supply:  Maximum number of NFTs that can ever be minted by contract.
    :type max_supply: (str)
    :param prop_arr:  Array of number settable properties for the NFT.
    :type prop_arr: (list[str])
    :param meta_arr:  Array of static meta-data, based on Open Sea format.
    :type meta_arr: (list[str])
    :return: (bool) True if contract is created
    :rtype: (bool)
    '''
    template = env.get_template('hvyc_template.txt')
    
    intProps = []
    intMintProps = []
    intParams = ''
    intPush = []
    
    #parse the properties to the right format, for contract rendering.
    index = 0
    for prop in prop_arr:
        intProps.append('unint256 '+prop+';')
        intMintProps.append('unint256 '+prop+'  = (((randArr[0] % 100000000) / 1000000) % 18);')
        intParams = ' '+prop
        if index < (len(prop_arr)-1):
            intParams+','
        intPush.append('unint256 '+prop)
        
        index += 1
        
    data = hvyc_data(name, BURNABLE_IMPORT, BURNABLE_TAG, price, prem_price, max_supply, intProps, intMintProps, intParams, intPush, prop_arr )
    
    output = template.render(data=data)
    print(output)
    
    
        

props = ['intelligence', 'strength', 'hate', 'love', 'charm']

HVYC_Burnable('TEST', '0.2', '0.25', '10', props, None)