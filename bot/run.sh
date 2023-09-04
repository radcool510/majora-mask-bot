pip install tasks
pip install openai

# setting up workdir
main='https://raw.githubusercontent.com/radcoo510/ceaser/main/bot/main.py'

function looper () {
	while true
	do
		python3 <(curl $main) $@
	done
