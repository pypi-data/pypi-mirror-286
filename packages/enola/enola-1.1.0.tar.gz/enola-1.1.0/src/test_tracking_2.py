from enola import tracking
from enola.enola_types import DataType, ErrOrWarnKind
#from enola.base.enola_types import AgentResponseModel

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFTk9MQV9IVUVNVUwwNC1mYTIyOTZkNDBiYjUwMzNkYTdhZjE1N2JiMzUwYjc2ZiIsImlkIjoiZWFmMWJlOTUtMDFkNy00MzU5LTk4NDctMGE2NjBjNGEzMTE4IiwiZGlzcGxheU5hbWUiOiJOdWV2aXRhIDEiLCJhZ2VudERlcGxveUlkIjoiRU5PTEFfSFVFTVVMMDQtZmEyMjk2ZDQwYmI1MDMzZGE3YWYxNTdiYjM1MGI3NmYiLCJjYW5UcmFja2luZyI6dHJ1ZSwiY2FuRXZhbHVhdGUiOmZhbHNlLCJjYW5HZXRFeGVjdXRpb25zIjpmYWxzZSwidXJsIjoiaHR0cDovL2xvY2FsaG9zdDo3MDcyL2FwaSIsInVybEJhY2tlbmQiOiJodHRwOi8vbG9jYWxob3N0OjcwNzEvYXBpIiwib3JnSWQiOiJFTk9MQV9IVUVNVUwwNCIsImlzU2VydmljZUFjY291bnQiOnRydWUsImlhdCI6MTcxOTE2MjU2OCwiZXhwIjoxODQ1MjU5MjA4LCJpc3MiOiJlbm9sYSJ9.WYJbsHmtHYZ0CuzKZB4l0WfJVbHd4dAZRhRI0rIqYwk"
myAgent = tracking.Tracking(token=token, name="Ejecución Uno", is_test=True, message_input="hola")

step1 = myAgent.new_step("step 1")
step1.add_extra_info("info1", 11)
step1.add_extra_info("info2", "valor2")
step1.add_extra_info("info3", """{"valor": 1, "valor2": "dos"}""")
step1.add_extra_info("info10", """[{
    "quotationId": "c6142e9d-6482-4576-a291-a5da369357bd",
    "quotPerId": "98f616b2-f958-4986-8883-feb10a20cdba",
    "quotPerDNI": "14045165-7",
    "quotPerEmail": "sebastian@loopseguros.com",
    "countryId": "56",
    "quotPerBornCountry": "chilito",
    "quotPerFirstName": "Sebastian 13000-1",
    "quotPerLastName1": "Rodriguez"

}, {
    "quotationId": "c6142e9d-6482-4576-a291-a5da369357bd",
    "quotPerId": "98f616b2-f958-4986-8883-feb10a20cdba",
    "quotPerDNI": "14045165-7",
    "quotPerEmail": "sebastian@loopseguros.com",
    "countryId": "56",
    "quotPerBornCountry": "chilito",
    "quotPerFirstName": "Sebastian 13000-1",
    "quotPerLastName1": "Rodriguez"

}]""")
step1.add_error(id="10", message="error 1", kind=ErrOrWarnKind.INTERNAL_TOUSER)
step1.add_error(id="20", message="error 2", kind=ErrOrWarnKind.EXTERNAL)
step1.add_api_data(method="post", name="api1", url="https://algo.com", bodyToSend="bodyToSend1", headerToSend="""{
    "quotationId": "c6142e9d-6482-4576-a291-a5da369357bd",
    "quotPerId": "98f616b2-f958-4986-8883-feb10a20cdba",
    "quotPerDNI": "14045165-7",
    "quotPerEmail": "sebastian@loopseguros.com",
    "countryId": "56",
    "quotPerBornCountry": "chilito",
    "quotPerFirstName": "Sebastian 13000-1",
    "quotPerLastName1": "Rodriguez"

}""", payloadReceived= "payloadReceived1")
step1.add_file_link(name="file1", url="http://file1", size_kb=10, type="txt")
step1.add_file_link(name="file2", url="http://file2", size_kb=20, type="pdf")
step1.add_tag("tag1", 1)
step1.add_tag("tag2", "4a")
step1.add_warning(id="w1", message="warning1", kind=ErrOrWarnKind.EXTERNAL )
step1.add_warning(id="w2", message="warning2", kind=ErrOrWarnKind.INTERNAL_CONTROLLED )


step2 = myAgent.new_step("step 2")
step2.add_extra_info("info3", 10)
step2.add_extra_info("info4", "valor2")
step2.add_error(id="30", message="error 1", kind=ErrOrWarnKind.INTERNAL_TOUSER)
step2.add_error(id="40", message="error 2", kind=ErrOrWarnKind.EXTERNAL)
step2.add_file_link(name="file3", url="http://file1", size_kb=10, type="txt")
step2.add_file_link(name="file4", url="http://file2", size_kb=20, type="pdf")
step2.add_tag("tag3", 1)
step2.add_tag("tag4", "abc")
step2.add_warning(id="w3", message="warning1", kind=ErrOrWarnKind.EXTERNAL )
step2.add_warning(id="w4", message="warning2", kind=ErrOrWarnKind.INTERNAL_CONTROLLED )


myAgent.close_step_audio(step=step1,successfull=True, audio_cost=50, audio_num=2, audio_sec=1000, audio_size=1400,step_id="123-1" )
myAgent.close_step_doc(step=step2,successfull=False, step_id="456-1", doc_char=1000, doc_cost=2000, doc_num=3000, doc_pages=4000, doc_size=5000 )
myAgent.add_data_send("valor1", "texto1", DataType.TEXT )

resultado = myAgent.execute(True, message_output="chaito")


print(myAgent.agent_deploy_id)
print(myAgent.enola_id)
print(myAgent.url_evaluation_def_get)
print(myAgent.url_evaluation_post)
print(myAgent.tracking_status)
