#coding: utf-8

def codeBlocksParser(data: str|bytes, language: str|bytes|list|None = None) -> list:
    import re
    # function to convert bytes to string
    def bytes_to_string(data: bytes) -> str:
        return data.decode()

    # function with regex to match code blocks into a string
    def match_code_blocks(data: str|bytes) -> list:
        return re.findall(r"```(.+?)```", data, re.DOTALL)

    # function to match single code blocks
    def match_single_code_blocks(data: str|bytes) -> list:
        # individual blocks delimited on same line only matched
        # exemple delimited : "`command line --option`"
        # the individual block is matched if it is on the same line, 
        # and after the delim of beginning and before the delim of end no "`" is found withoyt line return found
        return re.findall(r"`([^`\n]+)`", data)

    def split_code_block(code_block: str) -> dict:
        block = code_block.split('\n')
        # remove the first line if it is empty
        # and define the language if it is not defined
        if block[0] == '':
            language = None
            block = block[1:]
        elif block[0] != '':
            language = block[0]
            block = block[1:]
        # remove the last line if it is empty
        if block[-1] == '':
            block = block[:-1]
        return {
            'language': language,
            'code': '\n'.join(block)
        }

    def parse_blocks(data: str|bytes) -> dict:
        if type(data) == bytes:
            data = bytes_to_string(data)

        single_code_blocks = match_single_code_blocks(data)
        code_blocks = match_code_blocks(data)
        splited_code_blocks = [split_code_block(block) for block in code_blocks]
        return {
            'single_code_blocks': single_code_blocks,
            'code_blocks': splited_code_blocks
        }

    def keep_only_blocks_by_language(parsed_blocks: dict, language: str|bytes|list|None) -> dict:
        if language == None:
            return parsed_blocks
        elif type(language) == str:
            language = [language]
        elif type(language) == bytes:
            language = [language.decode()]

        keeped_blocks = []
        for parsed_block in parsed_blocks['code_blocks']:
            if parsed_block['language'] in language:
                keeped_blocks.append(parsed_block)
        return {
            'single_code_blocks': parsed_blocks['single_code_blocks'],
            'code_blocks': keeped_blocks
        }

    # ############# MAIN FUNCTION #############
    parsed_blocks = parse_blocks(data)
    return keep_only_blocks_by_language(parsed_blocks, language)
