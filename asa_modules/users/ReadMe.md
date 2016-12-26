<h3>Adding a local username</h3>

Once you have logged in just append a AsaUser object to the users field of the asa, and ensure that you pass the parent 
asa in.
    
    asa.users.append(
        AsaUser(asa, 'john', 'uber_pw', 15)
    )
        
<h3>Removing a local username</h3>

All you have to do is call the remove function on the users object in the asa and pass the index in.

    asa.users.remove(0)