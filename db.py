import os


DATABASE = 'pg_production'


def db2csv(query, filename):
    # ATTENTION : PostgreSQL fait la distinction entre :
    # - les guillemets doubles pour les noms de champs ;
    # - les guillemets simples pour les chaînes.
    os.system(r"""echo "COPY (%s) TO STDOUT with CSV HEADER" """
              r"""| psql %s -o '%s'""" % (query, DATABASE, filename))


def get_answers(challenge_id, filename):
    query = (r"""SELECT * from answers where """
             r"""\"challengeId\" = '%s'""" % challenge_id)
    db2csv(query, filename)
