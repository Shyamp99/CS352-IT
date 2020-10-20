0. Please write down the full names and netids of all your team members.
Kuber Sethi (KS1281), Shyam Patel (SPP128)


1. Briefly discuss how you implemented the LS functionality of
   tracking which TS responded to the query and timing out if neither
   TS responded.

We essentially had LS send out the query to both servers in the function accept_handler(). 
Due to how python socket.recv() works the program will wait until something forces the program to move forward. We fixed this issue using the select standard library.
The length of the two responses are then checked. The response for the ts server containin the query would not be an empty string while its counterpart would be an empty string.
We simply return the non empty response, if neither server has the query then None is returned.
LS then sends Client the aforementioned return value.



2. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain.

We are having issues getting the servers to run with non-blocking calls; however, in testing they worked with blocking calls. Non blocking calls
often give us issues such as sockets preemptively closing or errors like "Errno 115: Operation now in progress"


3. What problems did you face developing code for this project?

Being able to communnicate with each other due to quarantine whereas on campus it would be much easier and we would work more efficently.
We had issues with extremely slow and laggy ilabs due to high traffic.
In terms of code, we would often hit errors in trying to have our sockets work using non blocking calls. This would often lead to issues
such as sockets preemptively closing, error (specifically operation now in progress), and strange undefined behavior at times.



4. What did you learn by working on this project?

While working on this project we learned about how to have multiple sockets running on a single server as well as a way to 
implement a sort of timeout for each socket. We also learned a good amount from working with the libraries that we used