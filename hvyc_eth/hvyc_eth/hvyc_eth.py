"""
Heavy Meta HVYC & HVYI Ethereum Contract Handler.
Created on Wed Aug  3 12:20:54 2022

@author: meta-cronos
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from jinja2 import Environment, FileSystemLoader
import solcx
import json
import os

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
BURNABLE_IMPORT = 'import "./@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";'
BURNABLE_TAG = ' ERC721Burnable, '
UINT_256 = 'uint256 '
UINT_MINT = 'uint256 {{intProp}} = (((randArr[0] % 100000000) / 1000000) % 18);'

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
contract_template = 'hvy_template.txt'
sol_version = '0.8.4'

#Begin Contract Data Classes-----------------------------

@dataclass_json
@dataclass      
class hvym_base_data:
    '''
    Creates Base data array container object.
    :param intProps: List of strings used for the character struct.
    :type intProps:  (list[str])
    :param intMintProps: List of strings used for randomized mint properties.
    :type intMintProps:  (list[str])
    :param intParams: Concatenated string used for the premium mint method parameters.
    :type intParams:  (str)
    :param intPush: List of strings used for in the mint methods -> character.push
    :type intPush:  (list[str])
    :return: (Object) Containing data elements
    :rtype: (Object)
    '''
    intProps: []
    intMintProps: []
    intParams: str
    intPush: []

@dataclass_json
@dataclass      
class hvym_data:
    '''
    Creates data object to be used in jinja text renderer.
    :param model: String identifier for Class: Character / Immortal.
    :type model:  (str)
    :param abrev: String abreviation for Class: C / I.
    :type abrev:  (str)
    :param name: String identifier defined by the creator.
    :type name:  (str)
    :param payable: String identifier "payable"( minting anyone for a price), "onlyOwner(minted by owner for a price)"
    :type payable:  (str)
    :param burnable: bool if burnable or not.
    :type burnable:  (bool)
    :param burnable_import: String script tag for burnable.sol contract.
    :type burnable_import:  (str)
    :param burnable_tag: Tag used in contract definition.
    :type burnable_tag:  (str)
    :param price: Base price for the nft, with randomly generated number properties.
    :type price:  (str)
    :param prem_price: Base price for the nft, with user mintable number properties.
    :type prem_price:  (str)
    :param max_supply: Max number that can be minted by the contract.
    :type max_supply:  (str)
    :param int_props: List of strings used for the number properties in the character struct.
    :type int_props:  (list[str])
    :param int_mint_props: List of strings used for randomized mint properties.
    :type int_mint_props:  (list[str])
    :param int_params: Concatenated string used for the premium mint method parameters.
    :type int_params:  (str)
    :param int_push: List of strings used for in the mint methods -> character.push
    :type int_push:  (list[str])
    :param int_method_props: List of strings used property getter methods in the contract.
    :type int_methos_props:  (list[str])
    :return: (Object) Containing data elements
    :rtype: (Object)
    '''
    model: str
    abrev: str
    name: str
    payable: str
    burnable: False
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
def SolInstall(version):
    versions = solcx.get_installed_solc_versions()
    

    
    if not version in versions:
        solcx.install_solc(version)

def Compile(contract):
    compiled = solcx.compile_source(
        contract,
        output_values=["abi", "bin-runtime"],
        solc_version=sol_version,
        import_remappings=["@openzeppelin=C:/Users/pc/node_modules/@openzeppelin"]
    )
    
    print(compiled)
    

def HVYM_DATA(name, price, prem_price, max_supply, prop_arr, meta_arr):
    '''
    Creates Data object for HVYC contract based on passed parameters.
    Shaping string into proper format for the contract.
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
    :return: (Object) Containing data elements
    :rtype: (Object)
    '''
    obj = hvym_base_data([], [], '', [])   
    
    #parse the properties to the right format, for contract rendering.
    index = 0
    for prop in prop_arr:
        print(prop)
        obj.intProps.append(prop+';')
        obj.intMintProps.append(prop+'  = (((randArr[0] % 100000000) / 1000000) % 18);')
        
        if index < (len(prop_arr)-1):
            obj.intParams += ' uint256 '+prop+','
        else:
            obj.intParams += ' uint256 '+prop
            
        obj.intPush.append(prop)
        
        index += 1
        
    
    return obj


def HVYCharacter_Payable(name, price, prem_price, max_supply, prop_arr, meta_arr):
    '''
    Creates a payable, burnable HVYC ERC721 (C: Character / burnable) contract from 
    template based on passed parameters. Payable means: any address can pay to mint
    the NFT. Used for a character that has a limited life.  So that it may be burned, 
    when conditions of the game would cause it to expire / die / be killed.
    
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
    template = env.get_template(contract_template)
    obj = HVYM_DATA(name, price, prem_price, max_supply, prop_arr, meta_arr)
    
    intProps = obj.intProps
    intMintProps = obj.intMintProps
    intParams = obj.intParams
    intPush = obj.intPush
        
    data = hvym_data('Character', 'C', name, 'payable', True, BURNABLE_IMPORT, BURNABLE_TAG, price, prem_price, max_supply, intProps, intMintProps, intParams, intPush, prop_arr )
    
    output = template.render(data=data)
    print(output)
    Compile(output)
    
def HVYCharacter_OnlyOwner(name, price, prem_price, max_supply, prop_arr, meta_arr):
    '''
    Creates an owner only, burnable HVYC ERC721 (C: Character / burnable) contract from 
    template based on passed parameters. Owner only means only the issuing address can
    mint the NFT. Used for a character that has a limited life.  So that it may be 
    burned, when conditions of the game would cause it to expire / die / be killed.
    
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
    template = env.get_template(contract_template)
    obj = HVYM_DATA(name, price, prem_price, max_supply, prop_arr, meta_arr)
    
    intProps = obj.intProps
    intMintProps = obj.intMintProps
    intParams = obj.intParams
    intPush = obj.intPush
        
    data = hvym_data('Character', 'C', name, 'onlyOwner', True, BURNABLE_IMPORT, BURNABLE_TAG, price, prem_price, max_supply, intProps, intMintProps, intParams, intPush, prop_arr )
    
    output = template.render(data=data)
    print(output)
    Compile(output)
    
def HVYImmortal_Payable(name, price, prem_price, max_supply, prop_arr, meta_arr):
    '''
    Creates a payable, burnable HVYI (I: Immortal / not-burnable) ERC721 contract 
    from template based on passed. Payable means: any address can pay to mint
    the NFT. Used for a character that has an infinite life.  Cannot be burnt by 
    any condition of the game.
    
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
    template = env.get_template(contract_template)
    obj = HVYM_DATA(name, price, prem_price, max_supply, prop_arr, meta_arr)
    
    intProps = obj.intProps
    intMintProps = obj.intMintProps
    intParams = obj.intParams
    intPush = obj.intPush
        
    data = hvym_data('Immortal', 'I', name, 'payable', False, BURNABLE_IMPORT, BURNABLE_TAG, price, prem_price, max_supply, intProps, intMintProps, intParams, intPush, prop_arr )
    
    output = template.render(data=data)
    print(output)
    Compile(output)
    
def HVYImmortal_OnlyOwner(name, price, prem_price, max_supply, prop_arr, meta_arr):
    '''
    Creates a burnable HVYI (I: Immortal / not-burnable) ERC721 contract 
    from template based on passed. Owner only means only the issuing address can
    mint the NFT. Used for a character that has an infinite life.  Cannot be 
    burnt by any condition of the game.
    
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
    template = env.get_template(contract_template)
    obj = HVYM_DATA(name, price, prem_price, max_supply, prop_arr, meta_arr)
    
    intProps = obj.intProps
    intMintProps = obj.intMintProps
    intParams = obj.intParams
    intPush = obj.intPush
        
    data = hvym_data('Immortal', 'I', name, 'onlyOwner', False, BURNABLE_IMPORT, BURNABLE_TAG, price, prem_price, max_supply, intProps, intMintProps, intParams, intPush, prop_arr )
    
    output = template.render(data=data)
    print(output)
    Compile(output)
        

props = ['intelligence', 'strength', 'hate', 'love', 'charm']

SolInstall(sol_version)

HVYCharacter_OnlyOwner('TEST', '0.2', '0.25', '10', props, None)