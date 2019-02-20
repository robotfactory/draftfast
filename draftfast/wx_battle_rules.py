from draftfast.rules import RuleSet

WX_BATTLE = 'WX_BATTLE'

ROSTER_SIZE = {
	WX_BATTLE: {
		'HEAT': 10,
		'COLD': 10,
		'PRECIP': 10,
		'WIND': 10,
	}
}

SALARY_CAP = {
	WX_BATTLE: {
		'HEAT': 40_000,
		'COLD': 40_000,
		'PRECIP': 40_000,
		'WIND': 40_000,
	}
}

POSITIONS = {
	WX_BATTLE: {
		'HEAT': [
			['CITY', 1, 10],
		],
		'COLD': [
			['CITY', 1, 10],
		],
		'PRECIP': [
			['CITY', 1, 10],
		],
		'WIND': [
			['CITY', 1, 10],
		],
	}
}

WX_HEAT_RULE_SET = RuleSet(
    site=WX_BATTLE,
    league='HEAT',
    roster_size=ROSTER_SIZE[WX_BATTLE]['HEAT'],
    salary_max=SALARY_CAP[WX_BATTLE]['HEAT'],
    position_limits=POSITIONS[WX_BATTLE]['HEAT'],
    general_position_limits=[],
)

WX_COLD_RULE_SET = RuleSet(
    site=WX_BATTLE,
    league='COLD',
    roster_size=ROSTER_SIZE[WX_BATTLE]['COLD'],
    salary_max=SALARY_CAP[WX_BATTLE]['COLD'],
    position_limits=POSITIONS[WX_BATTLE]['COLD'],
    general_position_limits=[],
)

WX_PRECIP_RULE_SET = RuleSet(
    site=WX_BATTLE,
    league='PRECIP',
    roster_size=ROSTER_SIZE[WX_BATTLE]['PRECIP'],
    salary_max=SALARY_CAP[WX_BATTLE]['PRECIP'],
    position_limits=POSITIONS[WX_BATTLE]['PRECIP'],
    general_position_limits=[],
)

WX_WIND_RULE_SET = RuleSet(
    site=WX_BATTLE,
    league='WIND',
    roster_size=ROSTER_SIZE[WX_BATTLE]['WIND'],
    salary_max=SALARY_CAP[WX_BATTLE]['WIND'],
    position_limits=POSITIONS[WX_BATTLE]['WIND'],
    general_position_limits=[],
)
