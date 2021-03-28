from operator import itemgetter
import pymysql

connection_parameters = {'host': 'my_database_endpoint_at_region.rds.amazonaws.com', 'user': 'user_name',
                         'password': 'password_given', 'database': 'database_name'}


def process(staff_name, timing, day):
    """Queries against the database and gets the result
    
    Args:
        staff_name (str): Name of the staff
        timing (str): Timing of the Period (First hour, Second hour etc)
        day (str): Day of the week (Monday, Tuesday etc)
    
    Returns:
        str: The period for the queried data if available, else `'Free Hour'` is returned
    """
    with pymysql.connect(**connection_parameters) as conn, conn.cursor() as cur:
        res = cur.execute('''select p.period
    from timetable t
    join staff s on s.id = t.staff_id
    join days d on d.id =  t.day_id
    join periods p on p.id = t.period_id
    join timings ti on ti.id = t.timing_id
    where staff_name = %s and timing = %s and day = %s ''',
                          (staff_name, timing.title(), day.title()))  # Using Parameterization to avoid SQL Injection
        return list(cur)[0][0] if res else '"Free"'


def main(event, context):
    """Entry point called by Lex
    
    Args:
        event (dict): Dict consisting of all the necessary data (Intent, Slots) gathered from Lex
        context (LambdaContext): Lambda Context Object
    
    Returns:
        dict: The response for lex in the predefined format
    """
    staff_name, timing, day = itemgetter('staff_name', 'timing', 'day')(event['currentIntent']['slots'])
    res = process(staff_name, timing, day)
    message = f'The {timing} hour for {staff_name} on {day} is {res}'
    response = {
        "dialogAction":
            {
                "fulfillmentState": "Fulfilled",
                "type": "Close", "message":
                {
                    "contentType": "PlainText",
                    "content": message
                }
            }
    }
    return response
