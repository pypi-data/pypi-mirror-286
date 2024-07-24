import argparse

from ncclient import manager

import xml.dom.minidom

import xmltodict

import json

import os

import re

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.prompts import PromptTemplate

 

os.environ["GOOGLE_API_KEY"] = "AIzaSyDk77Vk0l8EXo2reVUBXuFCg5Xq-Qz--Z4"

 

gemini_llm = ChatGoogleGenerativeAI(model= "gemini-pro", temperature=0.2)

 

prompt_2 = PromptTemplate.from_template("""

//System: You are a netconf request xml creator. (No human like behaviour, explanation is allowed. You should give only and only the xml request without intentendation only!)

You will be provided a list of structures of the xml request that you need to create.

NOTE: The last element in the structure is the element to retrieve, so it's tag is a simple <tag/> without any children.

NOTE 2: Simplify the xml request as much as possible.

Example:

//USER: ['lldp(http://openconfig.net/yang/lldp) > config > hello-timer, ['app-hosting-cfg-data(http://cisco.com/ns/yang/Cisco-IOS-XE-app-hosting-cfg) > apps > app > application-name']

//SYSTEM: <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><lldp xmlns="http://openconfig.net/yang/lldp"><config><hello-timer/></config></lldp

            <app-hosting-cfg-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-app-hosting-cfg"><apps><app></application-name></app></apps></app-hosting-cfg-data></filter>

//USER: {xml_req}

//SYSTEM:

""")

 

namespace = ''

leafs = {}

 

def extractParams(router_data, attribute_path = "",  namespace = ""):

    global leafs

 

    if isinstance(router_data, dict):

        for key, value in router_data.items():

            if key == '@xmlns':

                namespace = value

                attribute_path += f"({value})"

                continue

 

            if isinstance(value, dict):

                if attribute_path != "":

                    cur_path = attribute_path + " > " + key

                else:

                    cur_path = key

                extractParams(value, cur_path, namespace)

 

            elif isinstance(value, list):

                for item in value:

                    if attribute_path != "":

                        cur_path = attribute_path + " > " + key

                    else:

                        cur_path = key

                    extractParams(item, cur_path, namespace)

            else:

                cur_path = attribute_path + " > " + key

 

                extract_ns_pattern = r'\(\s*(.*?)\s*\)'

 

                ns_in_cur_path = re.findall(extract_ns_pattern, cur_path)

                ns_in_cur_path =  ' > '.join(ns_in_cur_path)

 

                cur_path_without_ns = re.sub(extract_ns_pattern, '', cur_path)

               

                if leafs.get(cur_path_without_ns):

                    temp = [cur_path, ns_in_cur_path]

                    if temp not in leafs[cur_path_without_ns]:

                        leafs[cur_path_without_ns].append([cur_path, ns_in_cur_path])

                else:

                    leafs[cur_path_without_ns] = [[cur_path, ns_in_cur_path]]

       

    return leafs

 

def create_xml_request(selected_attributes):

    #loop done to retry if there is Google's gemini server error

    while True:

        print('\nSelected attributes: ')

        count = 1

        for attribute in selected_attributes:

            print(str(count), '. ',attribute)

            count += 1

 

        proceed = input('Do you want to proceed with these attributes? (y/n): ')

        if proceed.lower() == 'y':

            print('Creating the xml request...\n')

 

            attribute_structures = []

            for attribute in selected_attributes:

                attribute_structures.append(attribute)

 

            final_prompt = prompt_2.format(xml_req = str(attribute_structures))

            xml_req_filter = ''

 

            try:

                xml_req_filter = gemini_llm.invoke(final_prompt).content

           

                # print the xml request in a pretty format

                xml_req_filter_final = xml.dom.minidom.parseString(xml_req_filter).toprettyxml()

                print(xml_req_filter_final)

 

                with open('xml_request.xml', 'w') as f:

                    f.write(xml_req_filter_final)

 

                send_request = input('Do you want to send the request to the router? (y/n): ')

                if send_request.lower() == 'y':

                    # send the request to the router

                    response = manager.get(filter = xml_req_filter_final)

                    print('\n\n\n',response)

 

                    # parse the response

                    response_data = xmltodict.parse(response.xml)["rpc-reply"]["data"]

                    # print the response in a pretty format

                    print(f"{xml.dom.minidom.parseString(response.xml).toprettyxml()}")

                    # st.session_state.send_request = False

 

                    with open('xml_response.xml', 'w') as f:

                        f.write(xml.dom.minidom.parseString(response.xml).toprettyxml())

 

                    # convert the response to python dictionary

                    response_in_dict = xmltodict.parse(response.xml)

                    # retrieve leaf values from the  response_in_dict and print as key value pairs

                    # extractParams(response_in_dict, "")

                   

                    # with open("response_data.json", "w") as f:

                    #     json.dump(response_in_dict, f)

 

                    print('The attributes have been retrieved successfully!')

                break

               

            except Exception as e:

                print('Google Gemini Server Error while creating the xml request. Please try again.')

                print_error = input('Do you want to print the error message? (y/n): ')

                if print_error.lower() == 'y':

                    print(e)

               

                retry = input('Do you want to retry? (y/n): ')

                if retry.lower() == 'n':

                    break

 

def create_xml_without_llm(selected_attributes):

 

    request  = '<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">'

 

    for attribute in selected_attributes:

        attribute_components = attribute.split(' > ')

        for i in range(len(attribute_components)):

            #check if component has an opening and closing tag, if yes the include the contents inside the bracket as xmlns in that tag

            if '(' in attribute_components[i] and ')' in attribute_components[i]:

                tag_name, xmlns = attribute_components[i].split('(')

                xmlns = xmlns.split(')')[0]

                request += f'<{tag_name} xmlns="{xmlns}">'

            else:

                request += f'<{attribute_components[i]}>'

       

        #add the closing tags

        for i in range(len(attribute_components) - 1, -1, -1):

            if '(' in attribute_components[i] and ')' in attribute_components[i]:

                tag_name, xmlns = attribute_components[i].split('(')

                request += f'</{tag_name}>'

            else:

                request += f'</{attribute_components[i]}>'

   

    request += '</filter>'

    print(request)

 

def get_config_by_attr_name(manager):

 

    selected_attributes = set()

 

    while True:

        to_retrieve = input('Give the attribute name you want to retrieve: ')

        found = False

        paths_found = []

 

        for key in leafs.keys():

            #get last word of the key

            last_word = key.split()[-1]

 

            #checking after stripping the spaces of all preceding and succeeding white spaces

            if last_word.strip() == to_retrieve.strip():

                found = True

                paths_found.append(key)

       

        if found == False:

            print('Attribute not found. Please enter a valid attribute name.')

 

        elif len(paths_found) > 1:

            print('Multiple paths found for the attribute. Please select the correct path: ')

            count = 1

            for path in paths_found:

                print(str(count), '. ', path)

                count += 1

 

            selected_path = int(input('Enter the path number: '))

            selected_attributes.add(paths_found[selected_path - 1])

        elif len(paths_found) == 1:

            print('Attribute found: ', paths_found[0])

            selected_attributes.add(paths_found[0])

 

   

        proceed = input('\nDo you want to retrieve more attributes? (y/n): ')

        if proceed.lower() == 'n':

            break

   

    #print the selected attributes

    print('Selected attributes: ')

    count = 1

    for attribute in selected_attributes:

        print(str(count), '. ',attribute)

        count += 1

   

    confirm = input('Do you want to proceed with these attributes? (y/n): ')

    if confirm.lower() == 'y':

        print('Creating the xml request...\n')

        #create the xml request

        create_xml_request(selected_attributes)

        #create_xml_without_llm(selected_attributes)

 

def get_config_by_line_num(manager):

 

    # with open("leafs.txt", "r") as f:

    #     lines = f.readlines()

 

    print('Give the line number of the attribute you want to retrieve(from leafs.txt): ')

 

    selected_attributes = set()

       

    while True:

        line_number = int(input('Enter the line number: '))

        line_number -= 1

        if line_number >= len(leafs.items()):

            print('Invalid line number. Please enter a valid line number.')

        else:

            attribute = list(leafs.values())[line_number][0][0]

            selected_attributes.add(attribute)

            print('Attribute Selected: ', attribute)

        proceed = input('\nDo you want to retrieve more attributes? (y/n): ')

        if proceed.lower() == 'n':

            break

       

    create_xml_request(selected_attributes)

 

def main():

    print('Choose the Cisco Version of the Router: ')

    print('1. IOS XE')

    print('2. IOS XR')

    version = input('Enter the version of the router(1/2): ')

    # Command-line argument parsing

    parser = argparse.ArgumentParser(description='Cisco Router NETCONF script.')

    #parser.add_argument('--version', type=int, choices=[1, 2], required=True, help='Cisco router version: 1 for IOS XE, 2 for IOS XR.')

    parser.add_argument('--ip', type=str, required=True, help='IP address of the router.')

    parser.add_argument('--username', type=str, required=True, help='Username for the router.')

    parser.add_argument('--password', type=str, required=True, help='Password for the router.')

    args = parser.parse_args()

 

    ip = args.ip

    username = args.username

    password = args.password

    port = '830'

    device_params = {}

 

    if version == 1:

        print('\nIOS XE selected')

        device_params = {'name': 'iosxe'}

    elif version == 2:

        print('\nIOS XR selected')

        device_params = {'name': 'iosxr'}

 

    print('Details of the router:')

    print(f'IP Address: {ip}')

    print(f'Username: {username}')

    print(f'Router Port: {port}')

    print(f'Router Manufacturer: Cisco')

    masked_password =  '*' * len(password)

    print(f'Password: {masked_password}')

 

    proceed = input('Do you want to proceed? (y/n): ')

 

    if proceed.lower() == 'y':

        print('Retrieving the router information...\n')

 

        with manager.connect(

           host=ip,

             port=port,

             username=username,

             password=password,

             hostkey_verify=False, #for lab/testing purposes

             look_for_keys=False,  #for lab/testing purposes

             allow_agent=False,    #for lab/testing purposes

             device_params=device_params

        ) as m:

            all_params = m.get_config(source="running")

            # st.write(f"```{xml.dom.minidom.parseString(all_params.xml).toprettyxml()}")

            router_data = xmltodict.parse(all_params.xml)["rpc-reply"]["data"]

           

            #write the param data to a file in formated json

       

            # file = open("router_data.json", "r")

            # router_data = json.load(file)

           

            # extract all the leafs from the json tree

            extractParams(router_data, "")

 

            with open("leafs.txt", "w") as f:

                count = 1

                for key, value in leafs.items():

                    #f.write(f"{key} : {value}\n")

                    f.write(f"{count}. {key}\n")

                    count += 1

 

            print('The router information has been retrieved successfully!')

 

            #get_config_by_line_num(m)

            get_config_by_attr_name(m)

           

if __name__ == '__main__':
    main()
