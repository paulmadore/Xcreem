/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 * 
 * The contents of this file are subject to the Mozilla Public License
 * Version 1.1 (the "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 * 
 * Software distributed under the License is distributed on an "AS IS"
 * basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
 * License for the specific language governing rights and limitations
 * under the License.
 * 
 * The Original Code is Komodo code.
 * 
 * The Initial Developer of the Original Code is ActiveState Software Inc.
 * Portions created by ActiveState Software Inc are Copyright (C) 2000-2007
 * ActiveState Software Inc. All Rights Reserved.
 * 
 * Contributor(s):
 *   ActiveState Software Inc
 * 
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 * 
 * ***** END LICENSE BLOCK ***** */

#include <stdio.h>

#ifdef WIN32
#   include <windows.h>
#   include <direct.h>
#else
#   include <stdarg.h>
#   include <stdlib.h>
#   include <unistd.h>
#endif


#ifdef WIN32
    #define getcwd _getcwd
#endif


void logInfo(const char* format ...)
{
    FILE* flog = NULL;
    if ((flog = fopen("talk.log", "a")) == NULL) {
        exit(1);
    }

    va_list ap;
    va_start(ap, format);
    fprintf(flog, "talk: info: ");
    vfprintf(flog, format, ap);
    va_end(ap);

    fclose(flog);
}


void _sleepOneSecond()
{
#ifdef WIN32
    Sleep(1000);
#else
    system("sleep 1");
#endif
}


#ifdef WIN32
BOOL WINAPI _consoleHandler(DWORD CEvent)
{
//    char mesg[128];
    BOOL rv = FALSE;

    switch(CEvent)
    {
    case CTRL_C_EVENT:
//        MessageBox(NULL, "CTRL+C received!","CEvent",MB_OK);
        logInfo("CTRL+C received!\n");
        break;
    case CTRL_BREAK_EVENT:
//        MessageBox(NULL, "CTRL+BREAK received!","CEvent",MB_OK);
        logInfo("CTRL+BREAK received!\n");
        break;
    case CTRL_CLOSE_EVENT:
        MessageBox(NULL, "Program being closed!","CEvent",MB_OK);
        break;
    case CTRL_LOGOFF_EVENT:
        MessageBox(NULL, "User is logging off!","CEvent",MB_OK);
        break;
    case CTRL_SHUTDOWN_EVENT:
        MessageBox(NULL, "User is logging off!","CEvent",MB_OK);
        break;

    }
    return rv;
}
#endif


int main(int argc, char** argv)
{
    logInfo("start\n");

#ifdef SETVBUF
    if ( setvbuf(stdin, NULL, _IONBF, 0) != 0 ) {
        logInfo("setvbuf on stdin failed\n");
    }
    if ( setvbuf(stdout, NULL, _IONBF, 0) != 0 ) {
        logInfo("setvbuf on stdout failed\n");
    }
    if ( setvbuf(stderr, NULL, _IONBF, 0) != 0 ) {
        logInfo("setvbuf on stderr failed\n");
    }
#endif

#ifdef ASK
    char name[1000];
    fprintf(stdout, "What is your name?\n");
    fflush(stdout);
    fscanf(stdin, "%s", name);
    logInfo("name is '%s'\n", name);
    fprintf(stdout, "Your name is '%s'.\n", name);
#endif

#ifdef TALK
    int i;
    for (i = 0; i < 5; i++) {
        fprintf(stdout, "o%d", i);
        fprintf(stderr, "e%d", i);
#ifdef FLUSH
        fflush(stdout);
        fflush(stderr);
#endif
        _sleepOneSecond();
    }
#elif TALKLOTS
    int i,j;
    for (i = 0; i < 5; i++) {
    for (j = 0; j < 4000; j++) {
        fprintf(stdout, "o%d", i);
        fprintf(stderr, "e%d", i);
    }
#ifdef FLUSH
        fflush(stdout);
        fflush(stderr);
#endif
        _sleepOneSecond();
    }
#endif

#ifdef LOG
    // Log each argument to its line in log.log.
    FILE* flog = NULL;
    if ((flog = fopen("log.log", "w")) == NULL) {
        exit(1);
    }

    for (int k = 0; k < argc; ++k) {
        fprintf(flog, argv[k]);
        fprintf(flog, "\n");
    }

    fclose(flog);
#endif

#ifdef HELLO10
    int i;
    for (i = 0; i < 10; ++i) {
    	fprintf(stdout, "hello\n");
    }
#endif

#ifdef HELLO10NOEOL
    int i;
    for (i = 0; i < 9; ++i) {
    	fprintf(stdout, "hello\n");
    }
    fprintf(stdout, "hello");
#endif

#ifdef CWD
    char cwd[1024];
    getcwd(cwd, 1024);
    fprintf(stdout, "CWD is '%s'\n", cwd);
#endif

#ifdef ENV
    // Print the value of the TALK_ENV environment variable.
#ifdef WIN32
    char talkenv[1024];
    if (! GetEnvironmentVariable("TALK_ENV", talkenv, 1024)) {
    	talkenv[0] = '\0';
    }
#else
    char *talkenv = getenv("TALK_ENV");
#endif
    if (talkenv) {
        fprintf(stdout, "TALK_ENV is '%s'\n", talkenv);
    } else {
        fprintf(stdout, "TALK_ENV is ''\n");
    }
#endif

#ifdef HANG
#ifdef WIN32
    if (SetConsoleCtrlHandler((PHANDLER_ROUTINE)_consoleHandler,TRUE)==FALSE) {
	// unable to install handler... 
	// display message to the user
	fprintf(stderr, "Unable to install Console handler!\n");
	return -1;
    }
#endif

    while (1) {
        _sleepOneSecond();
    }
#endif

#ifdef CLOSE
    fclose(stdout);
    fclose(stderr);
#endif


    int retval = 0;
    if (argc > 1) {
        retval = atoi(argv[1]);
        logInfo("returning %d\n", retval);
    }

    logInfo("done\n\n");
    return retval;
}


//---- mainline for win32 subsystem:windows app
#ifdef WIN32
int WINAPI WinMain(
    HINSTANCE hInstance,      /* handle to current instance */
    HINSTANCE hPrevInstance,  /* handle to previous instance */
    LPSTR lpCmdLine,          /* pointer to command line */
    int nCmdShow              /* show state of window */
)
{
    return main(__argc, __argv);
}


#endif

