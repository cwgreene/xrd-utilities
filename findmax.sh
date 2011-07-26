awk "BEGIN{max = 0; maxline=0} 
{ 
	if(\$1 >= $2 && \$1 <= $3 && max < \$2){ 
		max=\$2; maxline = \$1; 
	}; 
} 
END{print(maxline,\"/\",max)}" $1
