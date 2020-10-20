class Tree:
    def __init__(self):
        self.head = DNS_BST('m')
    
    def add(self, node):
        domain_name = node.domain
        curr = self.head
        while curr is not None:
            if domain_name == curr.domain:
                return
            elif domain_name < curr.domain:
                if curr.left is None:
                    curr.left = node
                    return
                else:
                    curr = curr.left
            else:
                if curr.right is None:
                    curr.right = node
                    return
                else:
                    curr = curr.right

    def search(self, domain, curr):
        if curr == None:
            return False
        elif curr.domain == domain:
            return True
        else:
            return self.search(domain, curr.left) or self.search(domain, curr.right)

class DNS_BST:

    def __init__(self, domain, ip):
        self.domain = domain
        self.right = None
        self.left = None
        self.ip = ip


    