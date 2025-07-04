import mwscript_parser
import mwscript_lexer

def test_parse(text):
    print("Testing: " + str(text))
    try:
        result = mwscript_parser.parser.parse(text, lexer=mwscript_lexer.lexer)
        print("Result: " + str(result))
        return result
    except Exception as e:
        print("Error: " + str(e))

# Test cases
test_cases = [
    'Begin test "AA1_Henwen"->PositionCell, 1040, -240, -72.05, 0, "Ald Velothi, Outpost" End',
    'Begin test StopScript "_ivza_04_scr_glnecrotrap" End',
    'Begin test "_ivza_04_stc_hwentr_1"->Disable end',
    'Begin test Set Hen_Agility to ( ( "Player"->GetAgility ) / 2 ) End',
    'Begin test If ( DTNPS_Timer_Health >= 1 ) Return ElseIf ( DTNPS_Timer_Health >= 1 ) Return EndIf End',
    'Begin test Set DTNPS_Count_HealthExclusive to ( DTNPS_Count_HealthExclusive - 8 ) End',
    'Begin test If ( Player->GetLevel > BAR_Ulfgaar.ulfgaar_lvl ) Return EndIf End',
    'Begin test set BAR_Ulfgaar.ulfgaar_lvl to ( Player ->GetLevel ) End',
]

for test in test_cases:
    test_parse(test)
    print("-" * 50)