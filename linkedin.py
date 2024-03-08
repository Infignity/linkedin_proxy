import textwrap, calendar


def format_profile(included):
    # name, position, about and area
    profile = ""
    for item in included:
        if item['$type'] == "com.linkedin.voyager.identity.profile.Profile":
            profile = textwrap.dedent(f"""
                Name: {item.get('firstName')} {item.get('lastName')}
                Headline: {item.get('headline')}
                Industry name: {item.get('industry')}
                Location: {item.get('geoLocationName')} {item.get('geoCountryName')}
                Summary: {item.get('summary')}
            """)

    # experience
    experience = "Experiences:"
    for item in included:
        if item['$type'] == "com.linkedin.voyager.identity.profile.Position":
            company_name = item.get('companyName')
            description = item.get('description')
            location = item.get('locationName')
            title = item.get('title')
            time_period = item['timePeriod']
            time_period_str = format_time_period(time_period)

            experience += textwrap.dedent(f"""
                {title} at {company_name}
                {time_period_str}
                Location: {location}
            """)
            if description:
                experience += f"Job description: {description}\n"

    # education
    education = "Education:"
    for item in included:
        if item["$type"] == "com.linkedin.voyager.identity.profile.Education":
            degree = item.get("degreeName")
            school = item.get("schoolName")
                
            time_period = item['timePeriod']
            time_period_str = format_time_period(time_period)
            mini_edu = textwrap.dedent(f"""
                {school}
                Degree: {degree}
                {time_period_str}
            """)
            if item.get('activities'):
                mini_edu += f"Activities: {item.get('activities')}"

            if item.get('fieldOfStudy'):
                mini_edu += f"Field: {item.get('fieldOfStudy')}"
            
            if item.get('honors'):
                mini_edu += f"Honors: {item.get('honors')}"
                
            education += mini_edu + "\n"

    # skills
    skills = []
    for item in included:
        if item['$type'] == 'com.linkedin.voyager.identity.profile.Skill':
            skills.append(item.get('name'))
    skills = 'Skills:\n' + ', '.join(skills)

    return "\n".join([profile, experience, education, skills])


def format_time_period(time_period):
    start_date, end_date = None, None
    if time_period:
        if time_period.get('startDate'):
            start_date = str(time_period['startDate']['year'])
            if time_period['startDate'].get('month'):
                start_date = calendar.month_name[time_period['startDate']['month']] + ',' + start_date
        if time_period.get('endDate'):
            end_date = str(time_period['endDate']['year'])
            if time_period['endDate'].get('month'):
                end_date = calendar.month_name[time_period['endDate']['month']] + ',' + end_date
    
    date_str = ""
    if start_date: date_str += "From {start_date} "
    if end_date: date_str += "to {end_date}"
    return date_str