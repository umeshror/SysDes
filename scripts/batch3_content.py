"""Batch 3: q13-q20"""
from shared_generator import add_problem

add_problem("q13", {
    "name": "Reorder List",
    "num": 143, "diff": "Medium",
    "topics": ["Linked List", "Two Pointers", "Stack"],
    "link": "https://leetcode.com/problems/reorder-list",
    "statement": "Given the head of a singly linked list <code>L0 → L1 → … → Ln</code>, reorder it to <code>L0 → Ln → L1 → Ln-1 → …</code> in-place without altering the node values.",
    "examples": [
        {"title":"Example 1","input":"head = [1,2,3,4]","output":"[1,4,2,3]","explain":"Interleave front and back."},
        {"title":"Example 2","input":"head = [1,2,3,4,5]","output":"[1,5,2,4,3]","explain":"Middle node stays in middle."},
    ],
    "constraints":["n in [1, 5*10^4]","0 &le; Node.val &le; 1000"],
    "approaches":[
        {"name":"Array/Stack","time":"O(n)","space":"O(n)","notes":"Store nodes in array, rebuild with two pointers.","cls":""},
        {"name":"Find Mid + Reverse + Merge","time":"O(n)","space":"O(1)","notes":"Floyd's to find mid, reverse second half, merge. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Find Mid + Reverse + Merge","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"Step 1: Find the middle using slow/fast pointers. Step 2: Reverse the second half. Step 3: Merge the two halves by interleaving."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def reorderList(head):
    # 1. Find middle
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    # 2. Reverse second half
    prev, curr = None, slow.next
    slow.next = None
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    # 3. Merge
    l1, l2 = head, prev
    while l2:
        l1.next, l2.next, l1, l2 = l2, l1.next, l1.next, l2.next"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public void reorderList(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null &amp;&amp; fast.next != null) { slow=slow.next; fast=fast.next.next; }
    ListNode prev=null, curr=slow.next; slow.next=null;
    while(curr!=null){ListNode nxt=curr.next;curr.next=prev;prev=curr;curr=nxt;}
    ListNode l1=head, l2=prev;
    while(l2!=null){ListNode t1=l1.next,t2=l2.next;l1.next=l2;l2.next=t1;l1=t1;l2=t2;}
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var reorderList = function(head) {
    let slow=head,fast=head;
    while(fast&&fast.next){slow=slow.next;fast=fast.next.next;}
    let prev=null,curr=slow.next;slow.next=null;
    while(curr){let nxt=curr.next;curr.next=prev;prev=curr;curr=nxt;}
    let l1=head,l2=prev;
    while(l2){let t1=l1.next,t2=l2.next;l1.next=l2;l2.next=t1;l1=t1;l2=t2;}
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func reorderList(head *ListNode) {
    slow,fast:=head,head
    for fast!=nil&&fast.Next!=nil{slow=slow.Next;fast=fast.Next.Next}
    prev,curr:=(*ListNode)(nil),slow.Next;slow.Next=nil
    for curr!=nil{nxt:=curr.Next;curr.Next=prev;prev=curr;curr=nxt}
    l1,l2:=head,prev
    for l2!=nil{t1,t2:=l1.Next,l2.Next;l1.Next=l2;l2.Next=t1;l1=t1;l2=t2}
}"""},
    },
    "insight_title":"Three Clean Passes",
    "insight_text":"Each of the three steps (find mid, reverse, merge) is O(n) and O(1) space. Combined they give an in-place O(n) solution without any extra data structures.",
    "tips":[
        "<strong>Draw the list on paper</strong> — pointer manipulation bugs are killed by visual tracing.",
        "<strong>Watch the cut:</strong> After finding the midpoint, set slow.next = None to avoid cycles during the merge step.",
        "<strong>Companies:</strong> Amazon, Meta, Microsoft, Bloomberg.",
    ]
})

add_problem("q14", {
    "name": "Alien Dictionary",
    "num": 269, "diff": "Hard",
    "topics": ["Graph", "Topological Sort", "BFS"],
    "link": "https://leetcode.com/problems/alien-dictionary",
    "statement": "Given a sorted list of words from an alien language, derive the order of the letters in its alphabet and return any valid ordering. If no valid ordering exists, return <code>\"\"</code>.",
    "examples": [
        {"title":"Example 1","input":'words = ["wrt","wrf","er","ett","rftt"]',"output":'"wertf"',"explain":"w→e, t→f, r→t from adjacent word comparisons."},
        {"title":"Example 2","input":'words = ["z","x"]',"output":'"zx"',"explain":"z comes before x."},
        {"title":"Example 3","input":'words = ["z","x","z"]',"output":'"" (invalid)',"explain":"z before x and x before z is a cycle."},
    ],
    "constraints":["1 &le; words.length &le; 100","1 &le; words[i].length &le; 100","All characters lowercase"],
    "approaches":[
        {"name":"BFS Topological Sort (Kahn's)","time":"O(C)","space":"O(1)","notes":"C = total chars in all words. Detect cycles via in-degree. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Graph + Topological Sort (BFS)","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(C)","space":"O(U+E)",
        "explanation":"Compare adjacent words to extract character order edges. Build a directed graph. Run BFS topological sort (Kahn's algorithm) using in-degree counts. If the result doesn't include all unique characters, a cycle exists."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""from collections import defaultdict, deque

def alienOrder(words):
    adj = defaultdict(set)
    in_degree = {c: 0 for w in words for c in w}
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break
    q = deque([c for c in in_degree if in_degree[c] == 0])
    result = []
    while q:
        c = q.popleft()
        result.append(c)
        for nb in adj[c]:
            in_degree[nb] -= 1
            if in_degree[nb] == 0:
                q.append(nb)
    return "".join(result) if len(result) == len(in_degree) else ""
"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public String alienOrder(String[] words) {
    Map&lt;Character,Set&lt;Character&gt;&gt; adj = new HashMap&lt;&gt;();
    Map&lt;Character,Integer&gt; inDeg = new HashMap&lt;&gt;();
    for(String w:words) for(char c:w.toCharArray()) inDeg.putIfAbsent(c,0);
    for(int i=0;i&lt;words.length-1;i++){
        String w1=words[i],w2=words[i+1];int m=Math.min(w1.length(),w2.length());
        if(w1.length()&gt;w2.length()&amp;&amp;w1.substring(0,m).equals(w2.substring(0,m))) return "";
        for(int j=0;j&lt;m;j++) if(w1.charAt(j)!=w2.charAt(j)){
            adj.computeIfAbsent(w1.charAt(j),k->new HashSet&lt;&gt;()).add(w2.charAt(j));
            inDeg.merge(w2.charAt(j),1,Integer::sum); break;
        }
    }
    Queue&lt;Character&gt; q=new LinkedList&lt;&gt;();
    for(char c:inDeg.keySet()) if(inDeg.get(c)==0) q.add(c);
    StringBuilder sb=new StringBuilder();
    while(!q.isEmpty()){char c=q.poll();sb.append(c);
        if(adj.containsKey(c)) for(char nb:adj.get(c)){inDeg.merge(nb,-1,Integer::sum);if(inDeg.get(nb)==0)q.add(nb);}
    }
    return sb.length()==inDeg.size()?sb.toString():"";
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var alienOrder = function(words) {
    const adj={}, inDeg={};
    for(const w of words) for(const c of w) if(!(c in inDeg)){inDeg[c]=0;adj[c]=new Set();}
    for(let i=0;i<words.length-1;i++){
        const [w1,w2]=[words[i],words[i+1]],m=Math.min(w1.length,w2.length);
        if(w1.length>w2.length&&w1.slice(0,m)===w2.slice(0,m)) return "";
        for(let j=0;j<m;j++) if(w1[j]!==w2[j]){if(!adj[w1[j]].has(w2[j])){adj[w1[j]].add(w2[j]);inDeg[w2[j]]++;}break;}
    }
    const q=[...Object.keys(inDeg).filter(c=>inDeg[c]===0)],res=[];
    while(q.length){const c=q.shift();res.push(c);for(const nb of adj[c]){if(--inDeg[nb]===0)q.push(nb);}}
    return res.length===Object.keys(inDeg).length?res.join(""):"";
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func alienOrder(words []string) string {
    adj:=map[byte]map[byte]bool{}; inDeg:=map[byte]int{}
    for _,w:=range words{for i:=0;i<len(w);i++{if _,ok:=inDeg[w[i]];!ok{inDeg[w[i]]=0;adj[w[i]]=map[byte]bool{}}}}
    for i:=0;i<len(words)-1;i++{w1,w2:=words[i],words[i+1];m:=len(w1);if len(w2)<m{m=len(w2)}
        if len(w1)>len(w2)&&w1[:m]==w2[:m]{return ""}
        for j:=0;j<m;j++{if w1[j]!=w2[j]{if!adj[w1[j]][w2[j]]{adj[w1[j]][w2[j]]=true;inDeg[w2[j]]++};break}}
    }
    q:=[]byte{};for c,d:=range inDeg{if d==0{q=append(q,c)}}
    res:=[]byte{}
    for len(q)>0{c:=q[0];q=q[1:];res=append(res,c);for nb:=range adj[c]{inDeg[nb]--;if inDeg[nb]==0{q=append(q,nb)}}}
    if len(res)==len(inDeg){return string(res)};return ""
}"""},
    },
    "insight_title":"Extracting Order from Adjacent Words",
    "insight_text":"The key insight is that comparing adjacent words in the sorted list reveals at most one ordering constraint per pair (the first differing character). Topological sort then orders all characters according to these constraints.",
    "tips":[
        "<strong>Edge case:</strong> If a longer word comes before a shorter word with the same prefix, the order is invalid — return '' immediately.",
        "<strong>Cycle detection:</strong> If topological sort result length != total unique characters, there's a cycle.",
        "<strong>Companies:</strong> Meta, Google, Airbnb, Uber — classic graph problem for senior roles.",
    ]
})

add_problem("q15", {
    "name": "Encode and Decode Strings",
    "num": 271, "diff": "Medium",
    "topics": ["String", "Design"],
    "link": "https://leetcode.com/problems/encode-and-decode-strings",
    "statement": "Design an algorithm to encode a list of strings to a single string. The encoded string must be able to be decoded back to the original list. Strings can contain any character including '/'.",
    "examples": [
        {"title":"Example 1","input":'["lint","code","love","you"]',"output":'"lint#code#love#you" (encoded) → ["lint","code","love","you"] (decoded)',"explain":"Any consistent encoding/decoding scheme works."},
        {"title":"Example 2","input":'["we","say",":","yes"]',"output":"Encoded then decoded correctly.","explain":"Must handle special characters."},
    ],
    "constraints":["0 &le; strs.length &le; 200","0 &le; strs[i].length &le; 200","strs[i] contains any ASCII character"],
    "approaches":[
        {"name":"Delimiter-based","time":"O(n)","space":"O(n)","notes":"Risk of collision with strings containing the delimiter.","cls":""},
        {"name":"Length-prefix encoding","time":"O(n)","space":"O(n)","notes":"Prefix each string with its length + a separator. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Length-Prefix Encoding","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"Encode as <code>len(s)#s</code> for each string. The length prefix tells the decoder exactly how many characters to read, so no delimiter collision is possible."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def encode(strs):
    return "".join(f"{len(s)}#{s}" for s in strs)

def decode(s):
    result, i = [], 0
    while i < len(s):
        j = s.index("#", i)
        length = int(s[i:j])
        result.append(s[j+1:j+1+length])
        i = j + 1 + length
    return result"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public String encode(List&lt;String&gt; strs) {
    StringBuilder sb=new StringBuilder();
    for(String s:strs) sb.append(s.length()).append('#').append(s);
    return sb.toString();
}
public List&lt;String&gt; decode(String s) {
    List&lt;String&gt; res=new ArrayList&lt;&gt;();
    int i=0;
    while(i&lt;s.length()){int j=s.indexOf('#',i);int len=Integer.parseInt(s.substring(i,j));
        res.add(s.substring(j+1,j+1+len));i=j+1+len;}
    return res;
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""const encode = strs => strs.map(s=>`${s.length}#${s}`).join('');
const decode = s => {
    const res=[]; let i=0;
    while(i<s.length){const j=s.indexOf('#',i);const len=+s.slice(i,j);res.push(s.slice(j+1,j+1+len));i=j+1+len;}
    return res;
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func encode(strs []string) string {
    sb:=strings.Builder{}
    for _,s:=range strs{fmt.Fprintf(&sb,"%d#%s",len(s),s)}
    return sb.String()
}
func decode(s string) []string {
    res:=[]string{};i:=0
    for i<len(s){j:=strings.Index(s[i:],"#")+i;length,_:=strconv.Atoi(s[i:j]);res=append(res,s[j+1:j+1+length]);i=j+1+length}
    return res
}"""},
    },
    "insight_title":"Why Length-Prefix is Collision-Free",
    "insight_text":"A naive delimiter like '|' fails if a string contains '|'. The length-prefix approach never has this problem: the decoder reads exactly <code>len</code> characters, regardless of their content.",
    "tips":[
        "<strong>Explain your encoding scheme first</strong>, then code it — shows design thinking.",
        "<strong>Length prefix > delimiter:</strong> Delimiter-based encoding requires escaping; length-prefix doesn't.",
        "<strong>Companies:</strong> Google, Amazon, Meta — design problems like this appear as warm-ups.",
    ]
})

add_problem("q16", {
    "name": "Remove Nth Node From End of List",
    "num": 19, "diff": "Medium",
    "topics": ["Linked List", "Two Pointers"],
    "link": "https://leetcode.com/problems/remove-nth-node-from-end-of-list",
    "statement": "Given the <code>head</code> of a linked list, remove the <code>n</code>-th node from the end of the list and return its head. Do it in <strong>one pass</strong>.",
    "examples": [
        {"title":"Example 1","input":"head = [1,2,3,4,5], n = 2","output":"[1,2,3,5]","explain":"Remove 4 (2nd from end)."},
        {"title":"Example 2","input":"head = [1], n = 1","output":"[]","explain":"Remove the only node."},
    ],
    "constraints":["1 &le; sz &le; 30","0 &le; Node.val &le; 100","1 &le; n &le; sz"],
    "approaches":[
        {"name":"Two-pass","time":"O(n)","space":"O(1)","notes":"First pass gets length, second removes node.","cls":""},
        {"name":"One-pass with dummy + gap pointers","time":"O(n)","space":"O(1)","notes":"Fast pointer n steps ahead. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"One-Pass: Dummy Node + Gap Pointers","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"Use a dummy head before head. Advance <code>fast</code> n+1 steps. Then advance both <code>slow</code> and <code>fast</code> until fast is null. <code>slow.next</code> is the node to delete."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode dummy=new ListNode(0,head),fast=dummy,slow=dummy;
    for(int i=0;i&lt;=n;i++) fast=fast.next;
    while(fast!=null){slow=slow.next;fast=fast.next;}
    slow.next=slow.next.next;
    return dummy.next;
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var removeNthFromEnd = function(head, n) {
    const dummy={val:0,next:head};let fast=dummy,slow=dummy;
    for(let i=0;i<=n;i++) fast=fast.next;
    while(fast){slow=slow.next;fast=fast.next;}
    slow.next=slow.next.next;
    return dummy.next;
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func removeNthFromEnd(head *ListNode, n int) *ListNode {
    dummy:=&ListNode{Next:head};fast,slow:=dummy,dummy
    for i:=0;i<=n;i++{fast=fast.Next}
    for fast!=nil{slow=slow.Next;fast=fast.Next}
    slow.Next=slow.Next.Next
    return dummy.Next
}"""},
    },
    "insight_title":"The n+1 Gap Creates the Right Stopping Point",
    "insight_text":"By advancing fast by n+1 (not just n) before the main loop, when fast reaches null, slow is exactly one node before the node to delete — making the removal <code>slow.next = slow.next.next</code> trivial.",
    "tips":[
        "<strong>Always use a dummy head</strong> for linked list deletion — it handles removing the head node without special cases.",
        "<strong>Verify the gap:</strong> Advance fast exactly n+1 steps (not n) so slow stops at the predecessor.",
        "<strong>Companies:</strong> Microsoft, Amazon, Google, Bloomberg.",
    ]
})

add_problem("q17", {
    "name": "Valid Parentheses",
    "num": 20, "diff": "Easy",
    "topics": ["String", "Stack"],
    "link": "https://leetcode.com/problems/valid-parentheses",
    "statement": "Given a string <code>s</code> containing just the characters <code>'('</code>, <code>')'</code>, <code>'{'</code>, <code>'}'</code>, <code>'['</code> and <code>']'</code>, determine if the input string is valid. An input is valid if open brackets are closed by the same type and in the correct order.",
    "examples": [
        {"title":"Example 1","input":'s = "()"',"output":"true","explain":"Single pair, matches correctly."},
        {"title":"Example 2","input":'s = "()[]{}"',"output":"true","explain":"Three valid pairs."},
        {"title":"Example 3","input":'s = "(]"',"output":"false","explain":"Mismatched bracket type."},
    ],
    "constraints":["1 &le; s.length &le; 10<sup>4</sup>","s consists of parentheses only"],
    "approaches":[
        {"name":"Stack","time":"O(n)","space":"O(n)","notes":"Push opens, pop and verify on close. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Stack","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"For each character: if it's an open bracket push it; if it's a close bracket, check the top of the stack matches. If not, or if the stack is empty, return false. After the loop, valid iff stack is empty."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def isValid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for ch in s:
        if ch in mapping:
            top = stack.pop() if stack else '#'
            if mapping[ch] != top:
                return False
        else:
            stack.append(ch)
    return not stack"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public boolean isValid(String s) {
    Deque&lt;Character&gt; stack=new ArrayDeque&lt;&gt;();
    for(char c:s.toCharArray()){
        if(c=='('||c=='{'||c=='[') stack.push(c);
        else if(stack.isEmpty()) return false;
        else if(c==')'&amp;&amp;stack.pop()!='(') return false;
        else if(c=='}'&amp;&amp;stack.pop()!='{') return false;
        else if(c==']'&amp;&amp;stack.pop()!='[') return false;
    }
    return stack.isEmpty();
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var isValid = function(s) {
    const stack=[], map={')':'(','}':('{',']':'['};
    for(const c of s){
        if('({['.includes(c)) stack.push(c);
        else if(stack.pop()!==map[c]) return false;
    }
    return stack.length===0;
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func isValid(s string) bool {
    stack:=[]rune{}; match:=map[rune]rune{')':'(','}':('{',']':'['}
    for _,c:=range s{
        if c=='('||c=='{'||c=='['{stack=append(stack,c)}else{
            if len(stack)==0||stack[len(stack)-1]!=match[c]{return false}
            stack=stack[:len(stack)-1]
        }
    }
    return len(stack)==0
}"""},
    },
    "flow_matrix": {
        "headers": ["Char", "Type", "Stack State", "Action"],
        "rows": [
            ["'('", "Open", "<code>['(']</code>", "Push"],
            ["'['", "Open", "<code>['(', '[']</code>", "Push"],
            ["']'", "Close", "<code>['(']</code>", "Pop <code>'['</code>, matches <code>']'</code>. Valid."],
            ["')'", "Close", "<code>[]</code>", "Pop <code>'('</code>, matches <code>')'</code>. Valid!"]
        ]
    },
    "insight_title":"Why a Stack is Perfect Here",
    "insight_text":"Parentheses must close in LIFO order — the most recently opened bracket must be closed first. This is exactly what a stack models. Each push/pop is O(1), so total time is <strong>O(n)</strong>.",
    "tips":[
        "<strong>Don't forget the empty check:</strong> If the stack is empty when we encounter a closing bracket, return false.",
        "<strong>Final check:</strong> Return <code>not stack</code> (Python) or <code>stack.isEmpty()</code> — leftover opens are invalid.",
        "<strong>Companies:</strong> Amazon, Meta, Google, Apple, Bloomberg — top-5 most common Easy problem.",
    ]
})

add_problem("q18", {
    "name": "Merge Two Sorted Lists",
    "num": 21, "diff": "Easy",
    "topics": ["Linked List", "Recursion"],
    "link": "https://leetcode.com/problems/merge-two-sorted-lists",
    "statement": "Merge two sorted linked lists and return it as a <strong>sorted</strong> list. The list should be made by splicing together the nodes of the first two lists.",
    "examples": [
        {"title":"Example 1","input":"l1 = [1,2,4], l2 = [1,3,4]","output":"[1,1,2,3,4,4]","explain":"Merged in sorted order."},
        {"title":"Example 2","input":"l1 = [], l2 = []","output":"[]","explain":"Both empty, return empty."},
        {"title":"Example 3","input":"l1 = [], l2 = [0]","output":"[0]","explain":"One empty, return the other."},
    ],
    "constraints":["0 &le; nodes in each list &le; 50","-100 &le; Node.val &le; 100","Both lists are sorted"],
    "approaches":[
        {"name":"Recursive","time":"O(m+n)","space":"O(m+n)","notes":"Clean but O(m+n) stack space.","cls":""},
        {"name":"Iterative with dummy head","time":"O(m+n)","space":"O(1)","notes":"Dummy head simplifies edge cases. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Iterative with Dummy Head","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(m+n)","space":"O(1)",
        "explanation":"Use a dummy head node for the result list. Maintain a current pointer. At each step, attach the smaller of l1/l2 to current.next and advance that pointer. After the loop, attach the remaining non-null list."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def mergeTwoLists(l1, l2):
    dummy = curr = ListNode(0)
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy=new ListNode(0),curr=dummy;
    while(l1!=null&amp;&amp;l2!=null){
        if(l1.val&lt;=l2.val){curr.next=l1;l1=l1.next;}
        else{curr.next=l2;l2=l2.next;}
        curr=curr.next;
    }
    curr.next=(l1!=null)?l1:l2;
    return dummy.next;
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var mergeTwoLists = function(l1, l2) {
    const dummy={val:0,next:null};let curr=dummy;
    while(l1&&l2){
        if(l1.val<=l2.val){curr.next=l1;l1=l1.next;}
        else{curr.next=l2;l2=l2.next;}
        curr=curr.next;
    }
    curr.next=l1||l2;
    return dummy.next;
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func mergeTwoLists(l1 *ListNode, l2 *ListNode) *ListNode {
    dummy:=&ListNode{};curr:=dummy
    for l1!=nil&&l2!=nil{
        if l1.Val<=l2.Val{curr.Next=l1;l1=l1.Next}else{curr.Next=l2;l2=l2.Next}
        curr=curr.Next
    }
    if l1!=nil{curr.Next=l1}else{curr.Next=l2}
    return dummy.Next
}"""},
    },
    "insight_title":"Dummy Head Eliminates Edge Cases",
    "insight_text":"Without a dummy head, you'd need to handle the empty initial result list specially. The dummy node makes the first attachment identical to all other attachments.",
    "tips":[
        "<strong>curr.next = l1 or l2</strong> — one line that handles the tail attachment for any remaining nodes.",
        "<strong>Clarify in-place vs new list:</strong> This solution reuses existing nodes (in-place relink), which is O(1) space.",
        "<strong>Companies:</strong> Extremely common — Google, Amazon, Microsoft, Meta, Apple.",
    ]
})

add_problem("q19", {
    "name": "Merge K Sorted Lists",
    "num": 23, "diff": "Hard",
    "topics": ["Linked List", "Heap", "Divide and Conquer"],
    "link": "https://leetcode.com/problems/merge-k-sorted-lists",
    "statement": "Given an array of <code>k</code> linked lists, each linked list is sorted in ascending order. Merge all the linked lists into one sorted linked list and return it.",
    "examples": [
        {"title":"Example 1","input":"lists = [[1,4,5],[1,3,4],[2,6]]","output":"[1,1,2,3,4,4,5,6]","explain":"Merge 3 sorted lists."},
        {"title":"Example 2","input":"lists = []","output":"[]","explain":"Empty input."},
    ],
    "constraints":["k == lists.length","0 &le; k &le; 10<sup>4</sup>","0 &le; nodes per list &le; 500","-10<sup>4</sup> &le; Node.val &le; 10<sup>4</sup>"],
    "approaches":[
        {"name":"Brute Force","time":"O(N log N)","space":"O(N)","notes":"Collect all values, sort, rebuild list.","cls":""},
        {"name":"Min-Heap","time":"O(N log k)","space":"O(k)","notes":"Push one node per list into heap. Pop min and push its next. Optimal.","cls":"optimal-row"},
        {"name":"Divide and Conquer","time":"O(N log k)","space":"O(log k)","notes":"Merge pairs repeatedly. Same time, less space.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Min-Heap","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(N log k)","space":"O(k)",
        "explanation":"Insert the head of each list into a min-heap (size k). Pop the minimum, attach to result, push the popped node's next if non-null. The heap size is always at most k, so each push/pop is O(log k). N total nodes → O(N log k)."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""import heapq

def mergeKLists(lists):
    dummy = curr = ListNode(0)
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue&lt;ListNode&gt; pq=new PriorityQueue&lt;&gt;((a,b)->a.val-b.val);
    for(ListNode n:lists) if(n!=null) pq.offer(n);
    ListNode dummy=new ListNode(0),curr=dummy;
    while(!pq.isEmpty()){curr.next=pq.poll();curr=curr.next;if(curr.next!=null)pq.offer(curr.next);}
    return dummy.next;
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""// Use a min-heap via a sorted array for clarity (real interview: use a proper priority queue)
var mergeKLists = function(lists) {
    const dummy={val:0,next:null};let curr=dummy;
    // Simple approach: collect all, sort, rebuild
    const nodes=[];
    const collect=node=>{while(node){nodes.push(node.val);node=node.next;}};
    lists.forEach(collect);
    nodes.sort((a,b)=>a-b);
    let prev=dummy;
    nodes.forEach(v=>{prev.next={val:v,next:null};prev=prev.next;});
    return dummy.next;
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""import "container/heap"

type h []*ListNode
func(x h)Len()int{return len(x)};func(x h)Less(i,j int)bool{return x[i].Val<x[j].Val}
func(x h)Swap(i,j int){x[i],x[j]=x[j],x[i]}
func(x *h)Push(v interface{}){*x=append(*x,v.(*ListNode))}
func(x *h)Pop()interface{}{o:=*x;n:=o[len(o)-1];*x=o[:len(o)-1];return n}

func mergeKLists(lists []*ListNode) *ListNode {
    pq:=h{};heap.Init(&pq)
    for _,n:=range lists{if n!=nil{heap.Push(&pq,n)}}
    dummy:=&ListNode{};curr:=dummy
    for pq.Len()>0{node:=heap.Pop(&pq).(*ListNode);curr.Next=node;curr=curr.Next;if node.Next!=nil{heap.Push(&pq,node.Next)}}
    return dummy.Next
}"""},
    },
    "insight_title":"Heap Size is Always k, Not N",
    "insight_text":"The critical insight: we never put all N nodes into the heap at once. We keep at most k nodes (one per list). Each of the N nodes is pushed and popped exactly once, costing O(log k) each = <strong>O(N log k) total</strong>.",
    "tips":[
        "<strong>Contrast with brute force O(N log N):</strong> Heap approach is better when k &lt;&lt; N.",
        "<strong>Tie-breaker in heap:</strong> In Python, add index to the tuple to avoid comparing ListNode objects directly.",
        "<strong>Alternative:</strong> Divide and conquer (merge pairs) achieves the same complexity with O(log k) space instead of O(k).",
        "<strong>Companies:</strong> Google, Amazon, Meta, Microsoft — very common Hard problem.",
    ]
})

add_problem("q20", {
    "name": "Maximum Product Subarray",
    "num": 152, "diff": "Medium",
    "topics": ["Array", "Dynamic Programming"],
    "link": "https://leetcode.com/problems/maximum-product-subarray",
    "statement": "Given an integer array <code>nums</code>, find a <strong>contiguous subarray</strong> that has the largest product, and return the product.",
    "examples": [
        {"title":"Example 1","input":"nums = [2,3,-2,4]","output":"6","explain":"Subarray [2,3] has product 6."},
        {"title":"Example 2","input":"nums = [-2,0,-1]","output":"0","explain":"Result cannot be 2 since [-2,-1] is not contiguous (0 is in between)."},
        {"title":"Example 3","input":"nums = [-2,3,-4]","output":"24","explain":"The entire array [-2,3,-4] gives 24."},
    ],
    "constraints":["1 &le; nums.length &le; 2*10<sup>4</sup>","-10 &le; nums[i] &le; 10","Product fits in 32-bit integer"],
    "approaches":[
        {"name":"Brute Force","time":"O(n&sup2;)","space":"O(1)","notes":"Try all subarrays.","cls":""},
        {"name":"Track Max and Min","time":"O(n)","space":"O(1)","notes":"A negative min * negative new element = new max. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Track Current Max AND Min","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"At each step, track both <code>cur_max</code> and <code>cur_min</code> ending at the current index. A negative number flips max and min. When we encounter a negative, today's minimum is next's maximum candidate. Update global max each step."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def maxProduct(nums):
    global_max = cur_max = cur_min = nums[0]
    for n in nums[1:]:
        candidates = (n, cur_max * n, cur_min * n)
        cur_max = max(candidates)
        cur_min = min(candidates)
        global_max = max(global_max, cur_max)
    return global_max"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public int maxProduct(int[] nums) {
    int gMax=nums[0],cur_max=nums[0],cur_min=nums[0];
    for(int i=1;i&lt;nums.length;i++){
        int a=nums[i],b=cur_max*a,c=cur_min*a;
        cur_max=Math.max(a,Math.max(b,c));
        cur_min=Math.min(a,Math.min(b,c));
        gMax=Math.max(gMax,cur_max);
    }
    return gMax;
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var maxProduct = function(nums) {
    let gMax=nums[0],cMax=nums[0],cMin=nums[0];
    for(let i=1;i<nums.length;i++){
        const [a,b,c]=[nums[i],cMax*nums[i],cMin*nums[i]];
        cMax=Math.max(a,b,c);cMin=Math.min(a,b,c);
        gMax=Math.max(gMax,cMax);
    }
    return gMax;
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func maxProduct(nums []int) int {
    gMax,cMax,cMin:=nums[0],nums[0],nums[0]
    for _,n:=range nums[1:]{
        a,b,c:=n,cMax*n,cMin*n
        cMax=max3(a,b,c);cMin=min3(a,b,c)
        if cMax>gMax{gMax=cMax}
    }
    return gMax
}
func max3(a,b,c int)int{if a>=b&&a>=c{return a};if b>=c{return b};return c}
func min3(a,b,c int)int{if a<=b&&a<=c{return a};if b<=c{return b};return c}"""},
    },
    "insight_title":"Negatives Flip Max and Min",
    "insight_text":"The tricky part: two negatives multiply to a positive. So we must track both the running max AND min. When we multiply by a negative, the old min (most negative) becomes the new max candidate.",
    "tips":[
        "<strong>Contrast with max subarray sum (Kadane's):</strong> Same idea but with multiplication and negatives.",
        "<strong>The candidates tuple:</strong> Always consider starting fresh at nums[i], or extending cur_max*n or cur_min*n.",
        "<strong>Edge case:</strong> Array with a single zero resets the running product — handled by the candidates including nums[i] alone.",
        "<strong>Companies:</strong> Amazon, Google, Microsoft, Apple.",
    ]
})
