from drf_yasg import openapi

object_id_param = openapi.Parameter('object_id',
                                    openapi.IN_PATH,
                                    description="ID of an object.",
                                    type=openapi.TYPE_INTEGER)

# -- params for filters --
limit_param = openapi.Parameter('limit',
                                openapi.IN_QUERY,
                                description="Max number of returning of query rows. "
                                            "Set to -1 if you want to get all rows.",
                                type=openapi.TYPE_INTEGER,
                                default=50,
                                example=50)
offset_param = openapi.Parameter('offset',
                                 openapi.IN_QUERY,
                                 description="Number of skipping resulted query rows.",
                                 type=openapi.TYPE_INTEGER,
                                 default=0,
                                 example=0)
sort_by_param = openapi.Parameter('sort_by',
                                  openapi.IN_QUERY,
                                  description="Sort results by specified field.",
                                  type=openapi.TYPE_STRING,
                                  example='id')
sort_desc_param = openapi.Parameter('sort_desc',
                                    openapi.IN_QUERY,
                                    description="Sort results in descending order.",
                                    type=openapi.TYPE_BOOLEAN,
                                    example=True)
q_param = openapi.Parameter('q',
                            openapi.IN_QUERY,
                            description="Text search filter.",
                            type=openapi.TYPE_STRING)
date_to_param = openapi.Parameter('date_to',
                                  openapi.IN_QUERY,
                                  description="Show results before specified date.",
                                  type=openapi.TYPE_STRING,
                                  format=openapi.FORMAT_DATE,
                                  example='1789-04-25')
date_from_param = openapi.Parameter('date_from',
                                    openapi.IN_QUERY,
                                    description="Show results after specified date.",
                                    type=openapi.TYPE_BOOLEAN,
                                    format=openapi.FORMAT_DATE,
                                    example='1987-04-20')
object_id_filter_param = openapi.Parameter('object_id',
                                           openapi.IN_QUERY,
                                           description="ID search filter.",
                                           type=openapi.TYPE_INTEGER)
is_archived_param = openapi.Parameter('is_archived',
                                      openapi.IN_QUERY,
                                      description="Show only archive or only non archived fields.",
                                      type=openapi.TYPE_BOOLEAN,
                                      example=False)
status_param = openapi.Parameter('status',
                                 openapi.IN_QUERY,
                                 description="Show only results with same status.",
                                 type=openapi.TYPE_STRING)
# -- params for filters --
