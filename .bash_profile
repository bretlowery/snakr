# Setting PATH for Python 2.7
# The orginal version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}"
export PATH

# Setting PATH for Python 3.5
# The orginal version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.5/bin:${PATH}"
export PATH

export JAVA_HOME="$(/usr/libexec/java_home -v 1.8)"

# The next line updates PATH for the Google Cloud SDK.
source '/Users/bretlowery/google-cloud-sdk/path.bash.inc'

# The next line enables shell command completion for gcloud.
source '/Users/bretlowery/google-cloud-sdk/completion.bash.inc'

terminate(){
  lsof -P | grep ':80' | awk '{print $2}' | xargs kill -9 
  lsof -P | grep ':8080' | awk '{print $2}' | xargs kill -9
