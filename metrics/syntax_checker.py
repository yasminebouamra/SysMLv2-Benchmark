import sys

sys.path.insert(0,'C:/Users/z004x5km/OneDrive - Siemens AG/Desktop/Ressources ext/SysMLv2RepositoryClient/lib/python')

def syslmv2_syntax_checker_function(sysmlv2_textual_code: str):
    from dist import com_siemens_advsol_sysml_common_parser_SiemensParser as SiemensParser
    from dist import com_siemens_advsol_sysml_common_parser_Content as Content
    from dist import com_siemens_advsol_sysml_client_impl_SysMLv2RepositoryImpl as SysMLv2RepositoryImpl
    from dist import com_siemens_advsol_sysml_common_scope_impl_ProjectScopeBuilder as ProjectScopeBuilder
    from dist import com_siemens_advsol_sysml_common_util_Util as Util
    from dist import com_siemens_advsol_sysml_common_lang_DerivedPropertyHelper as DerivedPropertyHelper
    from dist import com_siemens_advsol_sysml_common_util_serialization_BaseSerialization as BaseSerialization
    from dist import com_siemens_advsol_sysml_common_util_Util as Util

    import re
    text_file = open("Example.sysml", "w")
    text_file.write(sysmlv2_textual_code)
    text_file.close()
    content = Content.withText("input.sysml", sysmlv2_textual_code)
    # content = Content.withStream("Example.sysml", File.read("Example.sysml"))
    #content = Content.withStream("Example.sysml", "package { hello }")
    parser = SiemensParser();

    # parser = RefImplParser()
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