def syslmv2_syntax_checker_function(sysmlv2_textual_code: str):
    from dist import com_siemens_advsol_sysml_common_parser_RefImplParser as RefImplParser
    from dist import com_siemens_advsol_sysml_common_parser_Content as Content
    from dist import sys_io_File as File
    import re
    
    text_file = open("Example.sysml", "w")
    text_file.write(sysmlv2_textual_code)
    text_file.close()
    content = Content.withStream("Example.sysml", File.read("Example.sysml"))
    #content = Content.withStream("Example.sysml", "package { hello }")

            
    parser = RefImplParser()
    result = parser.toJsonString([content])

    raw = parser.getLastLogData().stdout()
    x = re.findall("ERROR:(.*?)(?=\n|$)", str(raw))

    if not x:
        output = "the SysML V2 code contains no error"
    else:
        output ="Your code contains error:\n"
        for error in x:
            output = output + error.replace("Example.sysml","") + "\n"
    return(output)

def concrete_to_abstract(concrete_syntax : str):
    import sys
    import os
    import json
    sys.path.insert(0,'/home/alexandre/MBSE_Experiments/SysMLv2RepositoryClient/lib/python')
    sys.path.insert(0,'/home/alexandre/MBSE_Experiments/SysMLV2_Utilities')
    os.environ["TMP"] = "/home/alexandre/tmp"
    from dist import com_siemens_advsol_sysml_common_parser_RefImplParser as RefImplParser
    from dist import com_siemens_advsol_sysml_common_parser_Content as Content
    from dist import sys_io_File as File
    from dist import com_siemens_advsol_sysml_common_util_Util as Util
    from dist import com_siemens_advsol_sysml_common_parser_SiemensParser as SiemensParser
    Util.setTempDir("./tmp")
    content = Content.withText(text = concrete_syntax, name ="")
    parser = RefImplParser()
    #parser = SiemensParser()  # For now the T&I team advise to use the ref. implementation parser
    result = parser.toJsonString([content])
    return result