#
# OMNeT++/OMNEST Makefile for OMNeT_Tutorial
#
# This file was generated with the command:
#  opp_makemake -f --deep --nolink -O out -X. -L../../../inet/out/$$\(CONFIGNAME\)/src -lINET -KINET_PROJ=../../../inet
#

# Output directory
PROJECT_OUTPUT_DIR = ../../out
PROJECTRELATIVE_PATH = OmnetppProject/aloha
O = $(PROJECT_OUTPUT_DIR)/$(CONFIGNAME)/$(PROJECTRELATIVE_PATH)

# Other makefile variables (-K)
INET_PROJ=../../../inet

#------------------------------------------------------------------------------

# Pull in OMNeT++ configuration (Makefile.inc or configuser.vc)

ifneq ("$(OMNETPP_CONFIGFILE)","")
CONFIGFILE = $(OMNETPP_CONFIGFILE)
else
ifneq ("$(OMNETPP_ROOT)","")
CONFIGFILE = $(OMNETPP_ROOT)/Makefile.inc
else
CONFIGFILE = $(shell opp_configfilepath)
endif
endif

ifeq ("$(wildcard $(CONFIGFILE))","")
$(error Config file '$(CONFIGFILE)' does not exist -- add the OMNeT++ bin directory to the path so that opp_configfilepath can be found, or set the OMNETPP_CONFIGFILE variable to point to Makefile.inc)
endif

include $(CONFIGFILE)

# we want to recompile everything if COPTS changes,
# so we store COPTS into $COPTS_FILE and have object
# files depend on it (except when "make depend" was called)
COPTS_FILE = $O/.last-copts
ifneq ($(MAKECMDGOALS),depend)
ifneq ("$(COPTS)","$(shell cat $(COPTS_FILE) 2>/dev/null || echo '')")
$(shell $(MKPATH) "$O" && echo "$(COPTS)" >$(COPTS_FILE))
endif
endif

#------------------------------------------------------------------------------
# User-supplied makefile fragment(s)
# >>>
# <<<
#------------------------------------------------------------------------------

# Main target

all:   Makefile
	@# Do nothing

.PHONY: all clean cleanall depend msgheaders smheaders

msgheaders:

smheaders:

clean:
	$(qecho) Cleaning...
	$(Q)-rm -rf $O
	$(Q)-rm -f OMNeT_Tutorial OMNeT_Tutorial.exe libOMNeT_Tutorial.so libOMNeT_Tutorial.a libOMNeT_Tutorial.dll libOMNeT_Tutorial.dylib

cleanall: clean
	$(Q)-rm -rf $(PROJECT_OUTPUT_DIR)

depend:
	$(qecho) Creating dependencies...

