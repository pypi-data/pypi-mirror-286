from enola import evaluation
#from enola.enola_types import ErrOrWarnKind
#from enola.base.enola_types import AgentResponseModel

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFTk9MQV9IVUVNVUwwNC1mYTIyOTZkNDBiYjUwMzNkYTdhZjE1N2JiMzUwYjc2ZiIsImlkIjoiOWVjMTVlZDEtYTkzNy00ZTRlLTkwZTQtZmQ3YmNiMGRmOTg0IiwiZGlzcGxheU5hbWUiOiJudWV2aXRhIDEgLSBzb2xvIGV2YWx1YSIsImFnZW50RGVwbG95SWQiOiJFTk9MQV9IVUVNVUwwNC1mYTIyOTZkNDBiYjUwMzNkYTdhZjE1N2JiMzUwYjc2ZiIsImNhblRyYWNraW5nIjpmYWxzZSwiY2FuRXZhbHVhdGUiOnRydWUsImNhbkdldEV4ZWN1dGlvbnMiOmZhbHNlLCJ1cmwiOiJodHRwOi8vbG9jYWxob3N0OjcwNzIvYXBpIiwidXJsQmFja2VuZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NzA3MS9hcGkiLCJvcmdJZCI6IkVOT0xBX0hVRU1VTDA0IiwiaXNTZXJ2aWNlQWNjb3VudCI6dHJ1ZSwiaWF0IjoxNzE5MTYzNDY3LCJleHAiOjE4NDUyNTkyMDgsImlzcyI6ImVub2xhIn0.tIQvvOzmrcfDDKyen4d1Djxfvr-9XvMlR6wLl6l_8ag"
eval = evaluation.Evaluation(token=token)

eval.add_evaluation(enola_id="8c28bacd8b43bb74c0e070fb5145105c61c9623c4aef8fc5932af963f3d17171", eval_id="0", value=100, comment="eval 0, valor 1, AUTO")
eval.add_evaluation(enola_id="8c28bacd8b43bb74c0e070fb5145105c61c9623c4aef8fc5932af963f3d17171", eval_id="11", value=50, comment="eval 10, valor 2, AUTO")
#eval.add_evaluation(enola_id="7875bc29361e7ceff45258461fd16e4db4638c2fc73cb33e887dc40fff0047a92", eval_id="2'", value=3, comment="eval 2, valor 3")


result = eval.execute()

print ("total evals: ", result.total_evals)
print ("total errors: ", result.total_errors)


