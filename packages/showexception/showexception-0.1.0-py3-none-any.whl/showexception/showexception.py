#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Exception Handling Helpers
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

from quickcolor.color_def import colors

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def exception_details(e: Exception, area: str = 'unspecified', raw: bool = False) -> None:
    if raw:
        import traceback
        print(traceback.format_exc())
        return

    exceptionName = f"{colors.fg.lightred}{type(e).__name__}{colors.fg.lightgrey}"
    areaLabel = f"{colors.fg.cyan}{area}{colors.fg.lightgrey}"
    print(f"\n{exceptionName} exception occurred in {areaLabel} processing!")

    # exceptionArgs = e.args
    # for arg in exceptionArgs:
    for arg in e.args:
        print(f"{colors.fg.lightblue}--> {colors.off}{arg}")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

