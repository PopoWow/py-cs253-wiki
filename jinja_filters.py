
# add a filter for datetimes.  this might need to go in a more general area
def format_created(value):
    return value.strftime('%B %d, %Y')

def set_filters(env):
    env.filters['created'] = format_created

