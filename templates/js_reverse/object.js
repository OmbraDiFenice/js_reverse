{{ object_name }} = function(undefined) {

    obj = {
        patterns : {},
        
        DEBUG: false,
        
        reverse : function(name, args, kwargs) {
            if(this.reverse.arguments.length >= 1 && typeof name !== "string") throw "first argument must be a string"
            switch(this.reverse.arguments.length) {
            case 0: // no parameter specified
                throw "you must specify the name of the view to reverse at least"
                break;
            case 1: // just the name parameter
                args = [];
                kwargs = {};
                break;
            case 2: // second parameter can be args or kwargs
                if(typeof args !== 'object') throw "second parameter can be only an array (for positional arguments) or an object (for named arguments)"
                if(typeof args === 'object' && !Array.isArray(args)) {
                    kwargs = args;
                    args = [];
                } // else args is an array -> args = args
            break;
            case 3: // second parameter must be args, third paramter must be kwargs
                if(!Array.isArray(args)) throw "args must be an array";
                if(typeof kwargs !== 'object' || Array.isArray(kwargs)) throw "kwargs must be an object";
            break;
            }
        
            var address = this.patterns[name];
            if(address === undefined) throw "URL name \"" + name + "\" not found";
            if(this.DEBUG) {
                console.log("parsing view name " + name + "  raw address: " + address);
                console.log(" ");
            }
            for (var param in kwargs){
                if (kwargs.hasOwnProperty(param)) {
                    if(this.DEBUG) console.log("param: "+ param + "   kwargs[param]: " + kwargs[param]);
                    var start = address.indexOf("(?P<" + param +">");
                    if (start >= 0) {
                        if(this.DEBUG) console.log("named parameter \"" + param + "\" found");
                        parameter_regex = find_pattern.call(this, address, start);
                        address = address.replace(parameter_regex, kwargs[param]);
                        if(this.DEBUG) {
                            console.log("pattern after substitution: " + address);
                            console.log(" ");
                        }
                    } else if(this.DEBUG) {
                        console.log("no named parameter \"" + param + "\" found in pattern, skipping");
                        console.log(" ");
                    }
                    
                }
            }
            if(address.indexOf("(?P<") >= 0) throw "Pattern \"" + this.patterns[name] + "\" contains some uninitialized named parameters";
            
            for (var i = 0; i < args.length; i++) {
                if(this.DEBUG) console.log("param: "+ i + "   args[" + i + "]: " + args[i]);
                var start = address.search(/\((?!\?:)/);
                if (start >= 0) {
                    parameter_regex = find_pattern.call(this, address, start);
                    var end = start + parameter_regex.length;
                    address = address.substring(0, start) + args[i] + address.substring(end)
                    if(this.DEBUG) {
                        console.log("pattern after substitution: " + address);
                        console.log(" ");
                    }
                }
            }
            if(address.search(/\([^:]/) >= 0) throw "Pattern \"" + this.patterns[name] + "\" contains some uninitialized positional parameters (" + args.length + " provided)";
            
            return address;
        }
    };
    
    function find_pattern(address, start) {
        var opened_parenthesis = 1;
        var end;
        for(end = start+1; opened_parenthesis > 0; end++) {
            if(address[end] == ")" && address[end-1] != "\\") opened_parenthesis--;
            else if(address[end] == "(" && address[end-1] != "\\") opened_parenthesis++;
        }
        parameter_regex = address.substring(start, end);
        if(this.DEBUG) {
            console.log("start: " + start + "   address[start]: " + address[start]);
            console.log("end: " + end + "   address[end]: " + address[end]);
            console.log("parameter_regex: " + parameter_regex);
        }
        return parameter_regex;
    }
    
    return obj;
}();