config = {}

# this is default (site-packages\uvicorn\main.py)
config['log_config'] = "{
   "version":1,
   "disable_existing_loggers":true,
   "formatters":{
      "default":{
         "()":"uvicorn.logging.DefaultFormatter",
         "fmt":"%(levelprefix)s %(message)s",
         "use_colors":"None"
      },
      "access":{
         "()":"uvicorn.logging.AccessFormatter",
         "fmt":"%(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"
      }
   },
   "handlers":{
      "default":{
         "formatter":"default",
         "class":"logging.StreamHandler",
         "stream":"ext://sys.stderr"
      },
      "access":{
         "formatter":"access",
         "class":"logging.StreamHandler",
         "stream":"ext://sys.stdout"
      }
   },
   "loggers":{
      "uvicorn":{
         "handlers":[
            "default"
         ],
         "level":"INFO"
      },
      "uvicorn.error":{
         "level":"INFO",
         "handlers":[
            "default"
         ],
         "propagate":true
      },
      "uvicorn.access":{
         "handlers":[
            "access"
         ],
         "level":"INFO",
         "propagate":false
      }
   }
}

# add your handler to it (in my case, I'm working with quart, but you can do this with Flask etc. as well, they're all the same)
config['log_config']['loggers']['falcon'] =
{
   "handlers":[
      "default"
   ],
   "level":"INFO"
}
