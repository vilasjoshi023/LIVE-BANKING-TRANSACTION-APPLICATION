# Cassandra Performance Tuning with Solutions – searchable text transcription

> Source: user-provided PDF (115 pages). This Markdown file preserves extracted page text and page references for repository search. It does not reproduce the original PDF layout or embedded graphics. Use the source PDF for exact visual formatting.


## Source PDF page 1

    10.        Describe your experience with Cassandra's performance
       tuning.

Answer: Sample Answer (2–3 Minutes)

"I have worked extensively on Cassandra performance tuning in production
environments. My responsibilities included monitoring cluster health, identifying
performance bottlenecks, tuning JVM settings, optimizing compaction strategies,
resolving tombstone issues, improving data models, and performing capacity
planning.

Whenever we encountered a performance issue, I followed a structured
approach:

            1. Identify the symptom.
            2. Collect metrics using nodetool, Linux utilities, and monitoring
               dashboards.
            3. Find the root cause.
            4. Implement the fix.
            5. Monitor the cluster to ensure stability."




Scenario 1: High Read Latency Problem

The application team reported that read queries increased from 50 ms to
around 2–3 seconds.

               Investigation

o   First, I checked cluster health:
o   nodetool status
o   All nodes were UN.
o   Then I checked:
o   nodetool tablestats
    nodetool compactionstats

## Source PDF page 2

o   I also checked disk performance:
o   iostat -x 1
o   Using monitoring dashboards, I found:
o   High read latency
o   Large number of pending compactions
o   Increased disk utilization
o   Root Cause
o   A large number of SSTables and heavy compaction activity caused excessive
    disk reads.
o   Resolution
o   Increased compaction throughput
o   Optimized the compaction strategy
o   Scheduled heavy maintenance during off-peak hours
o   Result
o   Read latency dropped back to normal (around 60–80 ms).

let me understand deeply pin to pin explain
Scenario 1: High Read Latency Problem in Cassandra
The application team reported that read queries increased from 50 ms to around 2–3
seconds.
Let's go pin-to-pin, explaining what happened, why you checked each command,
what the output means, and how you decided on the solution.


Production Scenario
9:30 AM
Application team raises a P1 incident:
"Our application is very slow. Normally reads take 50 ms, but now they're taking 2–3
seconds."
At this point, you don't know the cause.
Possible causes include:
       Node down
       Network issue
       Disk issue
       JVM issue
       Compaction

## Source PDF page 3

        Large partitions
        Tombstones
        Hardware problem
Your job is to eliminate possibilities one by one.


Step 1: Check Cluster Health
First command:
nodetool status
Why?
Before checking performance, verify that the cluster itself is healthy.
Imagine a hospital:
        Before diagnosing a fever, first check if the patient is breathing.
Same concept.


Example output:
Datacenter: DC1
UN 10.10.10.1
UN 10.10.10.2
UN 10.10.10.3
UN 10.10.10.4
UN 10.10.10.5
Meaning
U = Up
N = Normal
So every node is:
        Running
        Connected
        Participating in the cluster
Conclusion
✅ Cluster is healthy.
Therefore, the issue is not caused by:
        Node failure
        Network partition
        Gossip failure

## Source PDF page 4

Move to the next step.


Step 2: Check Table Statistics
nodetool tablestats
Why?
The application says reads are slow.
Now you need to know which table is causing the issue.
This command provides:


        Read latency
        Write latency
        SSTable count
        Tombstone count
        Bloom filter usage
        Partition sizes




Suppose you see:
Read Latency


2500 ms
Normal is around:
40–80 ms
Conclusion
The problem is confirmed.


Then you notice:
SSTables per Read


45
Normal:
1–5
Why is this bad?
Suppose your data is stored in:

## Source PDF page 5

File1
File2
File3
...
File45
When a client requests one record, Cassandra may need to check many SSTables before
finding the latest version.
More SSTables = More disk reads = Slower queries.


Step 3: Check Compactions
Now run:
nodetool compactionstats
Why?
Compaction merges SSTables.
If too many compactions are running:
         Disk becomes busy
         Reads become slower


Example:
Pending Tasks


350
Normal:
0–10
What does "Pending Tasks" mean?
Imagine:
You have:
350 cleaning jobs waiting.
Cassandra cannot clean SSTables fast enough.
The queue keeps growing.


Think of it like:
One road.

## Source PDF page 6

Cars = Read requests


Bulldozers = Compactions
If many bulldozers are occupying the road,
Cars move slowly.
Exactly the same.


Conclusion
Compaction backlog exists.


Step 4: Check Disk Performance
Run:
iostat -x 1
Why?
Compaction reads and writes data continuously.
If the disk is already busy,
Read queries wait for disk access.


Example output:
%util


100%
Meaning
The disk is fully utilized.
No free I/O capacity.


Another important field:
await


200 ms
Normal:
1–5 ms
Meaning
Each disk request waits about 200 ms before it is serviced.

## Source PDF page 7

That is extremely slow.


Conclusion
The storage layer is the bottleneck.


Step 5: Check Monitoring Dashboard
Now open:
      Grafana
      Prometheus
      OpsCenter
You observe:
Read Latency


2500 ms
Disk Utilization


98%
Pending Compactions


350
Everything points to the same problem.


Root Cause Analysis
Now ask:
Why is the disk busy?
Because:
Too many SSTables
Why?
Because:
Compaction cannot keep up.
Why?
Possible reasons:
      Heavy write workload
      Compaction throughput too low

## Source PDF page 8

         Insufficient disk bandwidth
         Large SSTables
         Too few nodes


What Happens Internally?
Imagine the cluster has:
10 SSTables
Each write creates new SSTables.
After one hour:
25 SSTables
After three hours:
60 SSTables
Now a read request arrives.
Instead of checking:
File1
Cassandra checks:
File1


File2


File3


...


File60
That takes much longer.


Why Does Cassandra Need Compaction?
Because SSTables are immutable.
When data changes:
Old SSTable


+

## Source PDF page 9

New SSTable
Both exist.
Compaction merges them into:
One optimized SSTable
If compaction falls behind,
The number of SSTables keeps increasing.


Resolution
Solution 1
Increase compaction throughput.
Example in cassandra.yaml:
compaction_throughput_mb_per_sec
Suppose:
16 MB/sec
Increase to:
64 MB/sec
Now Cassandra cleans SSTables faster.


Solution 2
Review the compaction strategy.
For example:
Using:
SizeTieredCompactionStrategy
for time-series data may not be ideal.
Changing to:
TimeWindowCompactionStrategy
can reduce compaction overhead for that workload.


Solution 3
Move Heavy Operations
Avoid:
        Repairs
        Major compactions

## Source PDF page 10

       Bulk data loads
during business hours.
Schedule them at night.


Why Did Read Latency Improve?
Before:
Read


↓


45 SSTables


↓


Disk Busy


↓


2500 ms
After tuning:
Read


↓


4 SSTables


↓


Disk Free


↓


60 ms
Fewer SSTables mean fewer disk lookups, so queries complete much faster.

## Source PDF page 11

Interview Answer (Natural)


"When the application team reported that read latency increased from around 50 ms to 2–3
seconds, I first verified cluster health using nodetool status to ensure there were no failed
nodes. Next, I checked nodetool tablestats and found high read latency and an unusually
high number of SSTables per read. I then ran nodetool compactionstats, which showed a
large backlog of pending compactions. Using iostat -x 1, I confirmed the disks were
saturated with very high utilization and I/O wait times. From these observations, I
concluded that compaction could not keep up with the write workload, leading to too many
SSTables and excessive disk reads. We increased compaction throughput, reviewed the
compaction strategy, and moved heavy maintenance activities outside peak hours. After the
changes, the number of SSTables decreased, disk utilization normalized, and read latency
returned to approximately 60–80 ms."


This is the level of explanation interviewers expect from someone with production
Cassandra DBA experience

## Source PDF page 13

Scenario 2: High Write Latency Problem in Production.

The application experienced slow inserts during peak business hours.

              Investigation

o   Checked:
o   nodetool tpstats
    nodetool compactionstats
o   Observed:
o   High pending compactions
o   High disk I/O utilization
o   Root Cause
o   The storage subsystem could not keep up with the write workload.
o   Resolution
o   Added an additional Cassandra node
o   Rebalanced data across the cluster
o   Optimized compaction settings
o   Result
o   Write latency reduced significantly and throughput improved.

Production Scenario

Time: 11:30 AM
Application team calls:
"Our application is very slow while inserting data. Normally inserts take
20–30 ms, but now they're taking 1–2 seconds." This is called High Write
Latency.
At this point, you don't know the cause.
Possible reasons:
       Node down
       Disk issue
       Commit Log issue
       Compaction

## Source PDF page 14

   JVM GC
   Network
   High CPU
   Heavy write traffic
          Your job is to eliminate possibilities one by one.


          Step 1: Understand How Cassandra Writes Data
          Before troubleshooting, understand the write process.
          Application
               │
               ▼
          Coordinator Node
               │
               ▼
          Commit Log (Disk)
               │
               ▼
          Memtable (RAM)
               │
               ▼
          Acknowledgement to Client
               │
               ▼
          Flush to SSTable
               │
               ▼
          Compaction
          Normally this takes only 20–30 ms.
          Now it takes 2 seconds.
          Question:
          Where is the delay happening?


          Step 2: Check Thread Pools
          First command:

## Source PDF page 15

nodetool tpstats
Why?
Think of Cassandra as a company.
Every request is handled by workers (threads).
Suppose:
100 Employees


↓


5000 Customers arrive.
Employees cannot serve everyone immediately.
Customers wait in a queue.
Exactly the same happens inside Cassandra.


Example Output
Pool Name           Active Pending Completed


MutationStage           8       450         1200000


ReadStage           2           10         900000


CompactionExecutor          4        280      40000


Let's Understand Each Column
Active
Currently working threads
Example:
MutationStage


Active = 8
Meaning:
Eight write threads are busy.


Pending

## Source PDF page 16

Most important column.
Pending = 450
Meaning:
450 write requests are waiting.
Think of:
Restaurant


Chef = Cassandra Thread


Customers = Write Requests
Chef is cooking.
450 customers are waiting.
This is why inserts become slow.


First Conclusion
The cluster is overloaded.
But why?
We continue.


Step 3: Check Compactions
Now run:
nodetool compactionstats


Why?
Every write eventually creates SSTables.
More writes
↓
More SSTables
↓
More compactions


Example output

## Source PDF page 17

         pending tasks


         520
         Normal
         0–10
         520 means:
         Cassandra has 520 merge jobs waiting.


         Imagine:
         You have
         520 files


         waiting to be organized.
         The system cannot keep up.


         Step 4: Why Compactions Affect Writes
         Many beginners ask:
         "Compaction happens later. Why does it affect writes?"
         Excellent question.
         Imagine your laptop.
         You're copying
         100 GB
         from one folder to another.
         At the same time,
         you try copying another file.
         Will it be fast?
         No.
         Because the disk is already busy.
         Exactly the same in Cassandra.
         Compaction continuously:
   Reads SSTables
   Writes new SSTables
         The disk becomes busy.
         Now new writes arrive.

## Source PDF page 18

         They also need the same disk for:
   Commit Log
   Flushing Memtables
   Compactions
         Everything competes for disk I/O.


         Step 5: Verify Disk
         Run
         iostat -x 1


         Example
         Device


         %util = 100


         await = 180 ms


         Meaning of %util
         100%
         Disk is fully busy.
         Nothing else can be processed immediately.


         Meaning of await
         180 ms
         Each disk request waits 180 ms.
         Normally
         1–5 ms
         This is a huge delay.


         Step 6: Root Cause Analysis
         Now connect everything.
         Application says:
         Slow inserts
         Thread pool says:

## Source PDF page 19

         450 pending writes
         Compaction says:
         520 pending tasks
         Disk says:
         100% busy
         Everything points to one root cause.


         Root Cause
         The storage subsystem cannot process incoming writes fast
         enough.
         The disk is saturated because:
   Heavy write workload
   Too many compactions
   Limited disk bandwidth


         Why Add Another Node?
         Interviewer may ask:
         "Why didn't you just increase RAM?"
         Good question.
         Let's understand.
         Suppose one node can handle
         20,000 writes/sec
         Application suddenly generates
         40,000 writes/sec
         Can one node handle it?
         No.
         Now add another node.
         Now capacity becomes
         20,000


         +


         20,000

## Source PDF page 20

=


40,000 writes/sec
Load is shared.


Rebalancing
After adding a node,
existing nodes still contain most of the data.
Example:
Before
Node1


50 GB


Node2


50 GB


Node3


50 GB
Add Node4.
Initially
Node4


0 GB
Not balanced.
Data must be streamed.
After rebalance
Node1


37 GB


Node2

## Source PDF page 21

         38 GB


         Node3


         37 GB


         Node4


         38 GB
         Now every node shares work equally.


         Optimize Compaction
         Suppose
         Current setting
         compaction_throughput


         16 MB/sec
         Compaction is too slow.
         Increase to
         64 MB/sec
         Now Cassandra merges SSTables faster.
         Pending tasks reduce.


         Sometimes the problem is the compaction strategy.
         Example:
         Using
   SizeTieredCompactionStrategy
         for a time-series workload may create unnecessary compaction
         pressure.
         Switching to
   TimeWindowCompactionStrategy
         can reduce overhead.

## Source PDF page 22

After Fix
Before
Pending Writes


450


Pending Compactions


520


Disk Utilization


100%


Write Latency


2 sec
After adding a node and tuning compaction
Pending Writes


15


Pending Compactions


5


Disk Utilization


55%


Write Latency


25 ms
The application becomes responsive again.

## Source PDF page 23

Complete Troubleshooting Flow
Application Slow Inserts
       │
       ▼
Check Thread Pools
(nodetool tpstats)
       │
       ▼
Pending Writes High
       │
       ▼
Check Compactions
(nodetool compactionstats)
       │
       ▼
Pending Compactions High
       │
       ▼
Check Disk
(iostat -x 1)
       │
       ▼
Disk 100% Busy
       │
       ▼
Root Cause
Storage Bottleneck
       │
       ▼
Add New Node
       │
       ▼
Rebalance Data

## Source PDF page 24

       │
       ▼
Tune Compaction
       │
       ▼
Write Latency Restored
Interview Answer (Production Level)
"When the application team reported high write latency during peak
hours, I first checked nodetool tpstats and observed a large number
of pending write requests in the MutationStage, indicating the
cluster could not process writes quickly enough. Next, I checked
nodetool compactionstats and found a high backlog of pending
compactions. To confirm whether storage was the bottleneck, I
used iostat -x 1 and observed the disk utilization was close to 100%
with high I/O wait times. I concluded that the storage subsystem
was saturated because heavy write traffic and compaction were
competing for the same disk resources. To resolve the issue, we
added another Cassandra node to distribute the write load, allowed
the cluster to rebalance data across all nodes, and optimized the
compaction settings. After these changes, pending write requests
dropped significantly, disk utilization normalized, and write latency
returned to normal levels."

## Source PDF page 26

o   Scenario 3: Tombstone Problem
o   Problem
o   Some queries were timing out.
o   Application logs showed:
o   ReadTimeoutException
o   Investigation
o   Checked table statistics:
o   nodetool tablestats
o   Found a very high tombstone count.
o   Root Cause
o   Applications were frequently deleting records and using aggressive TTL
    values.
o   Resolution
o   Worked with developers to redesign the query pattern
o   Reduced unnecessary TTL usage
o   Optimized schema
o   Allowed compaction to clean obsolete tombstones
o   Result
o   Query execution time improved and timeouts disappeared.




              "What are tombstones? Have you faced tombstone issues in
              production? How did you resolve them?"
              Let's understand it from zero, just like a production engineer.


              Production Scenario
              Time: 2:00 PM
              Application team raises a ticket:
              "Some API calls are timing out. The application throws
              ReadTimeoutException."
              Normally:
              Read Time = 50 ms

## Source PDF page 27

          Now:
          Read Time = 10 seconds
          At this point, you don't know why.
          Possible reasons:
   Node down
   Disk issue
   JVM GC
   Network
   Large partitions
   Too many SSTables
   Tombstones
          Your job is to find the actual cause.


          Step 1: Understand What a Tombstone Is
          Many beginners think:
          DELETE removes data immediately.
          Wrong.
          Cassandra does not immediately delete data.
          Instead, it writes a tombstone (delete marker).
          Imagine a notebook.
          Instead of tearing out a page, you write:
          ❌ Deleted
          The page is still there, but marked as deleted.
          That's exactly how Cassandra works.


          Example
          Suppose the table contains:
          ID              Name
          1               John
          2               Ravi
          3               Alice
          Application runs:
          DELETE FROM employee WHERE id=2;

## Source PDF page 28

Does Cassandra remove the row?
No.
Internally it becomes:
ID                Name            Status
1                 John            Active
2                 Ravi            ❌ Tombstone
3                 Alice           Active


Why Doesn't Cassandra Delete Immediately?
Imagine you have 3 replicas.
Node1
Node2
Node3
Suppose Node3 is down.
Application deletes Ravi.
Node1 and Node2 receive DELETE.
Node3 is offline.
If Cassandra physically removed Ravi immediately,
when Node3 comes back,
it still has Ravi's record.
Now the cluster becomes inconsistent.
Instead,
Cassandra sends a tombstone.
Later,
Node3 receives the tombstone
and also marks Ravi as deleted.
Finally,
after the grace period and compaction,
the data is physically removed.
This prevents deleted data from coming back ("zombie data").


Step 2: Why Did the Application Timeout?
Application log shows:

## Source PDF page 29

ReadTimeoutException
Many candidates stop here.
A DBA continues investigating.


Step 3: Check Table Statistics
Run:
nodetool tablestats


Suppose output contains:
Average Tombstones Per Slice


250000
Normal:
0


10


100
But here:
250,000
Huge.


What Does This Mean?
Suppose one partition contains:
1000 Active Rows


+


250000 Tombstones
Application asks:
SELECT * FROM employee
WHERE department='HR';
Can Cassandra directly return data?
No.

## Source PDF page 30

It must examine every record.
Imagine:
Row1


Deleted


Row2


Deleted


Row3


Deleted


Row4


Deleted


...


250000 Deleted Rows


...


Finally


One Active Row
The database spends most of its time checking deleted markers
instead of returning live data.


Why Are Reads Slow?
Imagine searching a book.
Book A
100 pages

## Source PDF page 31

Book B
100 pages


+


25,000 blank pages
Which takes longer?
Obviously Book B.
Tombstones behave like those blank pages.


Step 4: Root Cause
Now ask:
Why are there so many tombstones?
Two common reasons:
Reason 1
Application deletes rows repeatedly.
Example:
DELETE FROM orders
WHERE order_id=100;
Thousands of DELETE operations every hour.


Reason 2
Aggressive TTL
Example:
INSERT INTO logs


USING TTL 60
Every record expires after 60 seconds.
Every expiry creates a tombstone.
Suppose application inserts:
100,000 rows/minute
After one minute,
all expire.
Now Cassandra creates:

## Source PDF page 32

100,000 tombstones
Every minute.
Very dangerous.


Step 5: Why Doesn't Compaction Remove Them
Immediately?
Excellent interview question.
Every tombstone has a grace period.
Typically:
gc_grace_seconds
Example:
864000


=


10 days
During those 10 days,
Cassandra keeps the tombstone
to ensure every replica learns about the delete.
Only after the grace period,
compaction can permanently remove it.


Step 6: Resolution
Fix 1
Meet application developers.
Explain:
Too many DELETE statements.
Instead of deleting frequently,
archive or redesign the workflow.


Fix 2
Reduce unnecessary TTL.
Bad:
TTL 60 seconds

## Source PDF page 33

Better:
TTL 7 days
or remove TTL if not required.


Fix 3
Improve Query Pattern
Bad query:
SELECT *


FROM logs
Better:
Query only the required partition and columns.
Avoid scanning partitions with large numbers of tombstones.


Fix 4
Optimize Schema
Suppose:
One partition stores:
5 Million Rows
Very bad.
Instead,
split data.
Example:
customer_id


+


month
Now each partition is much smaller.
Reads scan fewer tombstones.


Fix 5
Allow Compaction
Compaction merges SSTables.

## Source PDF page 34

After gc_grace_seconds expires,
obsolete tombstones are removed.
Over time:
250000 Tombstones


↓


1000


↓


50


↓


0


Before Fix
Application


↓


Read


↓


250000 Tombstones


↓


ReadTimeoutException


After Fix

## Source PDF page 35

          Application


          ↓


          Read


          ↓


          50 Tombstones


          ↓


          Query Completes


          ↓


          60 ms


          Why Did the Timeout Disappear?
          Because Cassandra no longer had to scan hundreds of thousands of
          tombstones before finding live rows.
          Less scanning means:
   Lower disk I/O
   Lower CPU usage
   Faster reads
   No ReadTimeoutException


          Complete Troubleshooting Flow
          Application Timeout
                 │
                 ▼
          ReadTimeoutException
                 │
                 ▼

## Source PDF page 36

Check nodetool tablestats
     │
     ▼
High Tombstone Count
     │
     ▼
Investigate Application
     │
     ▼
Frequent DELETE + Short TTL
     │
     ▼
Schema Review
     │
     ▼
Reduce TTL
     │
     ▼
Reduce DELETE Operations
     │
     ▼
Wait for gc_grace_seconds
     │
     ▼
Compaction Removes Tombstones
     │
     ▼
Read Performance Restored
Interview Answer (Senior DBA)
"The application team reported ReadTimeoutException for several
read queries. I first verified the cluster health and then checked
nodetool tablestats, where I observed an unusually high tombstone
count for the affected table. After reviewing the workload, I found
that the application was using very short TTL values and frequent

## Source PDF page 37

DELETE operations, both of which generated a large number of
tombstones. During reads, Cassandra had to scan those
tombstones before locating live data, which significantly increased
read latency and caused timeouts. I worked with the development
team to reduce unnecessary TTL usage, redesign the query and
data model to avoid scanning large partitions, and minimize DELETE
operations. After the gc_grace_seconds period elapsed, normal
compaction removed the obsolete tombstones. As a result, query
execution time improved substantially, and the read timeouts
disappeared."

## Source PDF page 39

o   Scenario 4: JVM Garbage Collection
o   Problem
o   Users experienced random latency spikes.
o   Investigation
o   Checked:
o   nodetool gcstats
o   and JVM statistics.
o   Observed:
o   Long GC pauses
o   Heap usage consistently above 90%
o   Root Cause
o   Heap pressure due to large workloads and object allocation.
o   Resolution
o   Tuned JVM heap configuration
o   Optimized G1 Garbage Collector settings
o   Reduced unnecessary object creation by improving workload distribution
o   Result
o   GC pauses reduced and latency stabilized.


              Excellent. This is one of the hardest Cassandra interview
              scenarios, because many people know what GC is, but they don't
              understand why GC causes latency.
Let's understand it exactly like a production DBA.


Production Scenario
Monday Morning - 10:30 AM
Application Team calls:
"Users are complaining that the application hangs for 5–10 seconds
randomly."
o   Notice the keyword:
o   Randomly
o   Sometimes:

## Source PDF page 40

o   Read Latency = 40 ms
o   After 5 minutes:
o   Read Latency = 7 seconds
o   Again:
o   Read Latency = 40 ms
o   Again:
o   Read Latency = 6 seconds
o   This is called Latency Spike.
o   The application is not always slow.
o   That is your first clue.


                Step 1: How Cassandra Runs
o   Many beginners think Cassandra directly runs on Linux.
o   Actually,
o   Linux OS
          │
          ▼
    Java Virtual Machine (JVM)
          │
          ▼
    Apache Cassandra
o   Everything Cassandra does happens inside JVM.


                Step 2: What Lives Inside JVM?
o   Imagine JVM is your bedroom.
o   Inside the room you keep
o   Bed
    Laptop
    Books
    Chair
    Clothes
o   Similarly JVM stores
o   Read Requests

## Source PDF page 41

    Write Requests


    Memtables


    Bloom Filters


    Indexes


    Cache


    Java Objects
o   Everything occupies memory.
o
o   Step 3: What is Heap?
o   Heap is simply
o   JVM Working Memory
o   Example
o   Server RAM
o   64 GB
o   JVM Heap
o   16 GB
o   That means Cassandra can use
o   16 GB
o   for Java objects.
o
o   Step 4: What Happens During Read?
o   Application sends
o   SELECT * FROM users
    WHERE id=100;
o   Cassandra creates Java objects.
o   Example
o   Query Object


    ↓

## Source PDF page 42

    Result Object


    ↓


    Connection Object


    ↓


    Buffer Object


    ↓


    Response Object
o   Every query creates objects.
o
o   Step 5: Thousands of Users
o   Imagine
o   One user
o   creates
o   10 Objects
o   Now
o   1000 users
o   ↓
o   10000 Objects
o   Now
o   10000 users
o   ↓
o   100000 Objects
o   Heap starts filling.
o
o   Step 6: Heap Usage
o   Initially

## Source PDF page 43

o   Heap


    □□□□□□□□□□


    10%
o   Later
o   Heap


    ■■□□□□□□□□


    40%
o   Later
o   Heap


    ■■■■■■■□□□


    70%
o   Later
o   Heap


    ■■■■■■■■■■


    95%
o   Almost full.
o
o   Step 7: What Happens When Heap is Full?
o   Imagine your office table.
o   Morning
o   Laptop


    Notebook
o   Enough space.
o   Evening

## Source PDF page 44

o   Laptop


    Notebook


    100 Files


    Coffee


    Keyboard


    Mouse


    Pens
o   No free space.
o   Can you work?
o   No.
o   First you clean the table.
o   Exactly same thing happens inside JVM.
o
o   Step 8: Garbage Collector Starts
o   Garbage Collector says
o   Memory almost full


    ↓


    Stop


    ↓


    Clean unused objects


    ↓


    Continue

## Source PDF page 45

o   This cleaning is called
o   Garbage Collection (GC)
o
o   Step 9: Why Application Becomes Slow?
o   Imagine restaurant.
o   Chef is cooking.
o   Suddenly
o   Manager says
o   Kitchen is dirty.


    Stop cooking.


    Clean kitchen.


    Then continue.
o   Customers wait.
o   Exactly same.
o   When GC starts,
o   Cassandra pauses.
o   During pause
o   No Reads
o   No Writes
o   No Responses
o   Users wait.
o
o   Step 10: Investigation
o   First command
o   nodetool gcstats
o   Example
o   Interval(ms)


    GC Count


    Max GC Time

## Source PDF page 46

    Total GC Time
o   Suppose
o   Max GC Time


    6500 ms
o   Meaning
o   One garbage collection took
o   6.5 seconds
o   Exactly matching application complaint.
o
o   Step 11: Check Heap
o   Using
o   JMX
o   Grafana
o   or JVM metrics
o   You see
o   Heap Used


    93%
o   Normal
o   50–70%
o   Anything above
o   90%
o   is dangerous.
o
o   Step 12: Why Did Heap Reach 93%?
o   Now ask
o   WHY?
o   Possible reasons
o
o   Reason 1
o   Huge Read Workload
o   Application suddenly receives

## Source PDF page 47

o   50000 Requests/sec
o   Every request creates Java objects.
o   Heap fills quickly.
o
o   Reason 2
o   Huge Write Workload
o   Large Memtables
o   Need more heap.
o
o   Reason 3
o   Large Queries
o   Bad query
o   SELECT *
    FROM orders;
o   Returns
o   2 Million Rows
o   JVM creates millions of Java objects.
o   Heap explodes.
o
o   Reason 4
o   Large Partitions
o   One partition
o   10 GB
o   Application reads
o   Entire partition.
o   Heap becomes full.
o
o   Reason 5
o   Caching
o   Too much cache.
o   Heap pressure increases.
o
o   Step 13: Root Cause
o   Heap pressure.

## Source PDF page 48

o   Meaning
o   JVM memory cannot keep up with workload.
o
o   Step 14: Resolution
o   Solution 1
o   Tune Heap
o   Current
o   Heap


    8 GB
o   Application doubled.
o   Increase
o   12 GB
o   or
o   16 GB
o   (Only if it matches Cassandra best practices—oversizing the heap can also
    increase GC pause times.)
o
o   Solution 2
o   Optimize G1 Garbage Collector
o   Modern Cassandra uses
o   G1GC
o   G1GC divides heap into small regions.
o   Instead of cleaning
o   Entire Heap
o   It cleans
o   Small Regions.
o   Less pause.
o
o   Solution 3
o   Reduce Object Creation
o   Bad
o   SELECT *
o   Good

## Source PDF page 49

o   SELECT


    name


    salary
o   Only required columns.
o   Less objects.
o   Less heap.
o
o   Solution 4
o   Improve Workload Distribution
o   Suppose
o   Node1
o   50000 Reads/sec
o   Node2
o   10000 Reads/sec
o   Node1 heap fills quickly.
o   Balance traffic.
o   Now
o   Node1
o   25000
o   Node2
o   25000
o   Heap pressure reduces.
o
o   Before Fix
o   Heap


    95%


    ↓


    GC Starts

## Source PDF page 50

    ↓


    Application Stops


    ↓


    Users Wait


    ↓


    Latency


    7 Seconds
o
o   After Fix
o   Heap


    65%


    ↓


    Small GC


    ↓


    No Pause


    ↓


    Read


    40 ms
o
o   Real Monitoring Dashboard

## Source PDF page 51

o   Before
o   Metric        o   Value
o   Heap          o   95%
o   Max GC Pause o    6500 ms
o   CPU           o   High
o   Read Latency o    7000 ms
o   After
o   Metric        o   Value
o   Heap          o   65%
o   Max GC Pause o    150 ms
o   CPU           o   Normal
o   Read Latency o    45 ms

o
o   Production Troubleshooting Flow
o   Users Report Random Slowness
             │
             ▼
    Check nodetool gcstats
             │
             ▼
    Long GC Pause Found
             │
             ▼
    Check Heap Usage
             │
             ▼
    Heap Above 90%
             │
             ▼
    Find Why Heap Is Full
             │
             ▼

## Source PDF page 52

    Large Queries
    Heavy Workload
    Large Partitions
    Too Many Objects
           │
           ▼
    Tune JVM Heap
           │
           ▼
    Tune G1GC
           │
           ▼
    Reduce Object Creation
           │
           ▼
    Balance Workload
           │
           ▼
    GC Pause Reduced
           │
           ▼
    Application Stable
o   Interview Answer (Senior DBA)
o   "When users reported random latency spikes, I suspected a JVM-related
    issue because the latency was intermittent rather than constant. I checked
    nodetool gcstats and observed long garbage collection pauses. JVM
    monitoring showed heap usage consistently above 90%, indicating significant
    heap pressure. I investigated the workload and found that large queries and
    heavy request volumes were creating many Java objects, forcing frequent
    and lengthy garbage collection cycles. We tuned the JVM heap according to
    Cassandra best practices, optimized the G1 Garbage Collector settings, and
    reduced unnecessary object creation by improving query patterns and
    balancing the workload across nodes. After these changes, heap utilization

## Source PDF page 53

stabilized, GC pause times dropped significantly, and application latency
returned to normal."
Give in HD Image

## Source PDF page 55

    Scenario 5: Uneven Data Distribution (Hot Partition) Problem
o   One Cassandra node consistently showed:
o   CPU: 95%
o   Other nodes: 20–30%
o   Investigation
o   Checked:
o   nodetool status
o   Reviewed the data model.
o   Root Cause
o   Poor partition key design caused one partition to receive most of the traffic.
o   Resolution
o   Worked with the application team to redesign the partition key so data was
    distributed evenly.
o   Result
o   CPU utilization became balanced across all nodes.
let me understand deeply pin to pin explain


Excellent. This is one of the top 5 Cassandra interview scenarios.
Companies like Infosys, Wipro, IBM, Capgemini, Cognizant, and banking clients
ask this because it tests whether you understand Cassandra data modeling,
not just DBA commands.
Let's understand it from scratch, like a real production incident.


Production Scenario
Monday Morning – 11:00 AM
The monitoring team calls:
"One Cassandra node is running at 95% CPU, but the other nodes are
only around 20–30%. The application is becoming slow."
Monitoring shows:
Node CPU
Node1 95% 🔴
Node2 22% 🟢

## Source PDF page 56

Node CPU
Node3 25% 🟢
Node4 28% 🟢
As a DBA, your first question should be:
Why is only one node busy?
If the cluster is healthy, the load should normally be shared.


Step 1: Understand How Cassandra Stores Data
Imagine you have 4 warehouses.
Warehouse1
Warehouse2
Warehouse3
Warehouse4
Customers place orders.
A manager decides:
"Which warehouse should store each order?"
In Cassandra, that "manager" is the Partition Key.


Step 2: What is a Partition Key?
The partition key decides:
Which node stores the data.
It is not random.
Cassandra:
   1. Takes the partition key.
   2. Calculates a hash value (token).
   3. Stores the data on the node responsible for that token.
Example:
PRIMARY KEY(customer_id)
Suppose:
customer_id = 101
Hash:
Token = 987654321
Token belongs to:
Node2

## Source PDF page 57

So that row is stored on Node2.


Step 3: Good Partition Key
Suppose your application has:
1 Million Customers
Each customer has a unique customer_id.
Example:
101
102
103
104
105
Hash values are different.
Data spreads like this:
Node1 → 250,000 rows


Node2 → 250,000 rows


Node3 → 250,000 rows


Node4 → 250,000 rows
Everything is balanced.
CPU:
25%
25%
25%
25%
Perfect.


Step 4: Bad Partition Key
Now imagine the developer creates this table:
PRIMARY KEY(country)
Application stores:

## Source PDF page 58

Country Users
India       5,000,000
USA         500
UK          300
Japan       250
Question:
Where will all Indian users go?
Answer:
One partition.
One node.


Imagine the warehouses.
Warehouse1


India Orders


5 Million
Warehouse2


USA Orders


500
Warehouse3


UK Orders


300
Warehouse4


Japan Orders


250
Which warehouse becomes overloaded?

## Source PDF page 59

Obviously:
Warehouse1
Exactly what happens in Cassandra.


Step 5: Why CPU Becomes 95%
Every application request for India goes to the same partition.
Every partition belongs to one primary replica.
So:
Read


↓


Node1
Write


↓


Node1
Again
Read


↓


Node1
Thousands of requests every second.
Node1 CPU:
95%
Other nodes:
Nothing much to do.


Step 6: Investigation
First command:
nodetool status
Output:

## Source PDF page 60

UN
UN
UN
UN
Meaning:
Cluster is healthy.
No node failure.
So why is Node1 busy?


Step 7: Open Grafana
You see:
Node1


CPU 95%


Disk Busy


Network Busy
Other nodes:
20%


Idle
This means:
Infrastructure is healthy.
Traffic is not balanced.


Step 8: Review Data Model
Now you ask the developers:
"What is the partition key?"
They show:
PRIMARY KEY(country)
Immediately you know the problem.


Step 9: Why This is Called a Hot Partition

## Source PDF page 61

One partition receives almost every request.
Example:
India


↓


10 Million Reads
USA
↓


200 Reads
UK
↓


100 Reads
Japan
↓


80 Reads
One partition becomes "hot".
Therefore:
One node becomes "hot".
Hence the term:
Hot Partition


Step 10: Why Doesn't Cassandra Automatically Balance It?
Many beginners ask:
"Cassandra has four nodes. Why doesn't it move some India data to another
node?"
Good question.
Because Cassandra's first rule is:
Same partition


↓

## Source PDF page 62

Must stay together.
It cannot split a single partition across multiple nodes.
So if the partition is huge,
that entire partition remains on one node.


Step 11: Resolution
You cannot fix this by changing Cassandra settings.
The real fix is:
Redesign the partition key.


Instead of:
PRIMARY KEY(country)
Use something that spreads data.
Example:
PRIMARY KEY((country, year), customer_id)
Now:
India-2024


↓


Node1
India-2025


↓


Node2
India-2026


↓


Node3
India-2027

## Source PDF page 63

↓


Node4
Now the load is distributed.


Another Example
Instead of:
customer_id
Use:
(customer_id, month)
Now one customer's yearly data is split into monthly partitions.
Instead of:
1 Huge Partition
You get:
January


↓


Node1


February


↓


Node2


March


↓


Node3
Smaller partitions.
Balanced load.

## Source PDF page 64

Step 12: Before Fix
Node1


CPU


95%
Node2


22%
Node3


20%
Node4


25%
Application latency:
High


Step 13: After Fix
After redesigning the partition key and migrating data:
Node1


46%
Node2


43%
Node3


48%
Node4


45%
Now every node shares the workload.

## Source PDF page 65

Why CPU Reduced
Before:
Every Read


↓


Node1
After:
Read1


↓


Node1


Read2


↓


Node2


Read3


↓


Node3


Read4


↓


Node4
Traffic is evenly distributed.
CPU becomes balanced.

## Source PDF page 66

Complete Troubleshooting Flow
Application Slow
     │
     ▼
Check Grafana
     │
     ▼
One Node CPU = 95%
     │
     ▼
Run nodetool status
     │
     ▼
Cluster Healthy
     │
     ▼
Review Data Model
     │
     ▼
Partition Key = country
     │
     ▼
Hot Partition Identified
     │
     ▼
Discuss with Developers
     │
     ▼
Redesign Partition Key
     │
     ▼
Migrate Data
     │
     ▼

## Source PDF page 67

CPU Balanced
     │
     ▼
Application Performance Improved
Interview Answer (Senior DBA)
"We observed that one Cassandra node consistently had around 95% CPU
utilization while the remaining nodes were between 20–30%. I first verified the
cluster health using nodetool status and confirmed all nodes were in the UN
state, so there was no infrastructure issue. I then reviewed monitoring metrics
and noticed that only one node was handling most of the read and write
requests. After discussing the schema with the application team, we found that
the partition key had very low cardinality, causing a hot partition. Since
Cassandra stores all rows of a partition together, that partition was mapped to a
single node, making it a bottleneck. We redesigned the partition key to
distribute data more evenly across the token range, migrated the data, and
validated the results. After the change, CPU utilization became balanced across
all nodes, request latency improved, and the hotspot was eliminated."


Interview Tip
When an interviewer asks "How do you identify a hot partition?", answer in
this order:
   1. Symptoms: One node has much higher CPU, disk I/O, or latency than
      others.
   2. Verification: Check cluster health (nodetool status) and monitoring
      dashboards.
   3. Analysis: Review the data model and partition key design.
   4. Root Cause: Low-cardinality or poorly chosen partition key created a hot
      partition.
   5. Resolution: Redesign the partition key and redistribute the data. This
      structured approach demonstrates production-level troubleshooting
      experience.

## Source PDF page 69

    Scenario 6: Pending Compactions Increasing Problem
o   Pending compactions continued to increase.
o   Investigation
o   nodetool compactionstats
o   Example:
o   Pending Tasks: 500
o   Root Cause
o   Write traffic exceeded the cluster's compaction capacity.
o   Resolution
o   Added nodes to the cluster
o   Increased available storage bandwidth
o   Tuned concurrent compactions
o   Result
o   Pending compactions gradually returned to normal levels.
    let me understand deeply pin to pin explain


Excellent. This is one of the most common production incidents for a
Cassandra DBA. Interviewers ask this because it tests whether you understand
how writes, SSTables, disks, and compaction work together.
    Let's go step by step like a real production engineer.


Production Scenario Tuesday – 3:00 PM
    The monitoring team raises an alert:
"Pending compactions have increased from 5 to 500, and the
application is becoming slow."
    Your Grafana dashboard shows:
    Metric                    Normal       Current
    Pending Compactions       5            500 🔴
    Read Latency              40 ms        1.5 sec 🔴
    Write Latency             20 ms        800 ms 🔴
    Disk Utilization          45%          98% 🔴

## Source PDF page 70

As a DBA, your first question is:
What is a pending compaction?


Step 1: Understand What Compaction Is
Imagine your office.
Every employee writes notes during the day.
Morning


Notebook1
Notebook2
Notebook3
Notebook4
By evening:
Notebook1
Notebook2
Notebook3
Notebook4
Notebook5
Notebook6
Notebook7
Notebook8
Too many notebooks.
The manager says:
"Combine these notebooks into one organized file."
That process is Compaction.


Step 2: How Cassandra Writes Data
Every write follows this path:
Application
    │
    ▼
Commit Log
    │
    ▼

## Source PDF page 71

Memtable (RAM)
       │
       ▼
Flush
       │
       ▼
SSTable
Suppose the application receives 1 million writes.
Cassandra creates many SSTables.
Example:
SSTable1
SSTable2
SSTable3
SSTable4
SSTable5
...
Too many SSTables are bad for read performance.


Step 3: Why Compaction Is Needed
Compaction merges many small SSTables into fewer large ones.
Before compaction:
20 SSTables
After compaction:
3 SSTables
Benefits:
     Faster reads
     Less disk usage
     Removes obsolete data and tombstones


Step 4: What Is a Pending Compaction?
Think of compaction as workers cleaning files.
Suppose you have:
Workers = 4
But cleaning jobs arrive like this:

## Source PDF page 72

100 Jobs
Four workers cannot finish immediately.
So jobs wait in a queue.
That queue is:
Pending Compactions


Step 5: Investigation
Run:
nodetool compactionstats
Example:
pending tasks: 500


What Does "500" Mean?
It does NOT mean Cassandra is running 500 compactions.
It means:
500 compaction jobs are waiting.
Only a few are running.
The remaining jobs are waiting for CPU and disk resources.


Step 6: Why Did Pending Compactions Increase?
Ask yourself:
Why are jobs arriving faster than they finish?
Imagine:
Workers can clean:
100 files/hour
But new files arrive:
500 files/hour
Queue grows:
Hour 1 → 400 waiting


Hour 2 → 800 waiting


Hour 3 → 1200 waiting
Exactly the same in Cassandra.

## Source PDF page 73

Step 7: Why Can't Cassandra Keep Up?
Reason 1: Heavy Write Traffic
Application suddenly increases from:
10,000 writes/sec
to
50,000 writes/sec
Every flush creates more SSTables.
More SSTables mean more compactions.
Compaction cannot keep up.


Reason 2: Slow Disk
Compaction needs to:
    Read old SSTables
    Write new SSTables
If the storage is slow:
Disk Speed


100 MB/sec
but workload needs:
400 MB/sec
The queue grows.


Reason 3: Too Few Nodes
Example:
Three-node cluster.
Application traffic doubles.
Each node now processes twice as many writes.
Compactions also double.
The cluster is undersized.


Step 8: What Happens If You Ignore It?
Many people think:
"Compaction is only cleanup."

## Source PDF page 74

Wrong.
Suppose:
Today:
10 SSTables
Tomorrow:
100 SSTables
Next week:
500 SSTables
Now a read request arrives.
Instead of checking:
3 SSTables
Cassandra checks:
500 SSTables
Reads become very slow.


Step 9: Confirm Disk Bottleneck
Run:
iostat -x 1
Example:
%util = 99%


await = 180 ms
Meaning:
The disk is almost fully busy.
Compactions cannot finish quickly.


Step 10: Root Cause
Now connect the information:
Application
↓
Heavy Writes
↓
Many Memtable Flushes
↓

## Source PDF page 75

Many SSTables
↓
Many Compactions
↓
Disk Cannot Keep Up
↓
Pending Tasks = 500
↓
Read & Write Latency Increase


Step 11: Resolution
Solution 1: Add More Nodes
Current cluster:
3 Nodes


↓


90,000 writes/sec
Application now generates:
150,000 writes/sec
Three nodes are overloaded.
Add two more nodes.
Now:
5 Nodes


↓


Each node processes fewer writes.
Compaction load is also distributed.


Solution 2: Increase Storage Bandwidth
Old storage:
200 MB/sec
Upgrade to:

## Source PDF page 76

800 MB/sec SSD/NVMe
Now compactions finish much faster.


Solution 3: Tune Concurrent Compactions
Cassandra controls how many compactions run simultaneously.
If the server has:
   Multiple CPU cores
   Fast SSDs
You can safely increase concurrent compactions so more cleanup jobs run in
parallel.
Important: Don't simply increase this value without considering CPU and
disk capacity. Too many concurrent compactions can make performance
worse.


Step 12: After the Fix
Before:
Pending Tasks


500


Disk Utilization


99%


Read Latency


1.5 sec


Write Latency


800 ms
After:
Pending Tasks

## Source PDF page 77

8


Disk Utilization


55%


Read Latency


45 ms


Write Latency


25 ms
Everything returns to normal.


Complete Production Flow
Application Traffic Increases
        │
        ▼
More Writes
        │
        ▼
More Memtable Flushes
        │
        ▼
More SSTables Created
        │
        ▼
More Compaction Jobs Needed
        │
        ▼
Disk Cannot Keep Up
        │
        ▼

## Source PDF page 78

Pending Compactions = 500
       │
       ▼
Read & Write Latency Increase
       │
       ▼
Check nodetool compactionstats
       │
       ▼
Check Disk (iostat)
       │
       ▼
Add Nodes
Increase Storage Speed
Tune Concurrent Compactions
       │
       ▼
Pending Compactions Return to Normal


Interview Answer (Senior Cassandra DBA)
"The monitoring system alerted us that pending compactions had increased
from normal levels to around 500. I first confirmed this using nodetool
compactionstats and then checked disk performance with iostat -x 1. The
disk utilization was close to 100%, indicating that compactions could not
complete as quickly as new SSTables were being created. The write workload
had increased significantly, producing SSTables faster than the storage
subsystem could merge them. To resolve the issue, we expanded the cluster
by adding nodes to distribute the write load, improved storage throughput,
and carefully tuned concurrent compaction settings based on the server's
CPU and disk capabilities. As the cluster caught up, the pending compaction
queue dropped to normal levels, and both read and write latencies returned
to expected values."
Interview Tip
A very common follow-up question is:

## Source PDF page 79

"Can I simply increase concurrent_compactors to solve pending
compactions?"
The correct answer is:
No. Increasing concurrent compactions without sufficient CPU and disk
bandwidth can make performance worse because more compaction threads
compete for the same resources. First identify the bottleneck (CPU, disk, or
workload), then tune compaction settings only if the underlying hardware
can support additional parallel work.

## Source PDF page 81

Scenario 7: Disk Full Problem
o   One Cassandra node reached 95% disk utilization.
o   Investigation
o   df -h
o   du -sh /var/lib/cassandra/*
o   Root Cause
o   Rapid data growth combined with old snapshots consuming space.
o   Resolution
o   Removed obsolete snapshots
o   Extended storage capacity
o   Planned additional nodes as part of capacity planning
o   Result
o   Disk utilization reduced and cluster stability was restored.
    let me understand deeply pin to pin explain
    Excellent. This is one of the most common real production incidents for
    a Cassandra DBA. Interviewers ask this because they want to know if you
    understand how Cassandra stores data on disk, how snapshots work,
    and why disk-full conditions are dangerous.
    Let's go pin-to-pin.


    Production Scenario
    Friday – 9:00 AM
    Monitoring generates a Critical Alert:
    Node-3 Disk Usage = 95%
    Application team hasn't reported issues yet.
    But as a DBA, you know:
    If disk reaches 100%, Cassandra can stop accepting writes and may
    even shut down.
    This becomes a P1 incident.


    Step 1: Why is Disk Space Important in Cassandra?
    Let's understand how Cassandra stores data.

## Source PDF page 82

Application
     │
     ▼
Commit Log
     │
     ▼
Memtable
     │
     ▼
Flush
     │
     ▼
SSTable (Disk)
Everything eventually ends up on disk.
Disk stores:
   SSTables
   Commit Logs
   Snapshots
   Hints
   Saved Caches
   Logs
If the disk is full:
   No new SSTables can be written.
   Commit Logs cannot grow.
   Writes fail.


Step 2: Monitoring Alert
Grafana shows:
Node        Disk Usage
Node1       60%
Node2       62%
Node3       95% 🔴
Node4       61%

## Source PDF page 83

Question:
Why only Node3?


Step 3: Check Disk Usage
Run:
df -h
Example:
Filesystem    Size Used Avail Use%


/dev/xvda1


500G


475G


25G


95%


What does this mean?
Disk size:
500 GB
Used:
475 GB
Available:
25 GB
Very dangerous.


Step 4: Find What is Using Space
Now run:
du -sh /var/lib/cassandra/*
Example:
420G data

## Source PDF page 84

50G snapshots


5G commitlog


2G hints


1G saved_caches
Now you know where the disk is going.


Understanding Every Directory
1. data/
420 GB
This contains:
   SSTables
   Actual database records
This is expected.


2. commitlog/
Stores:
Recent writes
Usually:
Small.


3. hints/
Stores:
Hinted Handoff data.
Usually:
Very small.


4. saved_caches/
Stores cache files.
Very small.


5. snapshots/

## Source PDF page 85

This is interesting.
50 GB
Question:
Why?


Step 5: What is a Snapshot?
Suppose before upgrading Cassandra,
you run
nodetool snapshot
Cassandra creates
Snapshot1
Next month
Another upgrade
↓
Snapshot2
Next month
↓
Snapshot3
Nothing deletes them automatically.


Imagine your phone.
You take:
Vacation Photos


2023


2024


2025
Never delete them.
Eventually:
Phone storage becomes full.
Snapshots behave exactly like that.

## Source PDF page 86

Step 6: Verify Snapshots
Check
find /var/lib/cassandra/data -name snapshots
Example
table1/snapshots/


table2/snapshots/


table3/snapshots/
You discover
50 GB
of snapshots.


Step 7: Root Cause Analysis
Question:
Why did disk become 95%?
There are two reasons.


Reason 1
Rapid Data Growth
Application traffic increased.
Example:
Last month
100 GB
Today
420 GB
Database is growing quickly.


Reason 2
Old Snapshots
Backup snapshots were never removed.
Example:
Snapshot1

## Source PDF page 87

10 GB


Snapshot2


15 GB


Snapshot3


25 GB
Total:
50 GB
Wasted space.


Step 8: Why is 95% Dangerous?
Imagine your laptop.
Storage:
500 GB
Only
5 GB
free.
Now copy
10 GB
file.
Can Windows save it?
No.
Exactly same.
Cassandra cannot create
New SSTables
↓
Writes fail.


Step 9: Resolution
Solution 1
Remove Old Snapshots

## Source PDF page 88

List snapshots:
nodetool listsnapshots
Remove them:
nodetool clearsnapshot
Immediately:
50 GB
becomes free.


Solution 2
Extend Storage
Suppose
Current
500 GB
Increase to
1 TB
Now Cassandra has room for future growth.


Solution 3
Capacity Planning
Don't wait until 95%.
Normally monitor:
60%


↓


70%


↓


80%
At
75–80%
Start planning:
    New nodes

## Source PDF page 89

   More storage
   Data rebalancing


Why Add New Nodes?
Many interviewers ask:
"Why not just increase disk size?"
Good question.
Suppose
Current cluster
3 Nodes


420 GB each
Add one node.
Data becomes
Node1


315 GB


Node2


320 GB


Node3


310 GB


Node4


315 GB
Benefits:
   Less disk usage
   Less CPU
   Better read/write performance
   Better fault tolerance

## Source PDF page 90

Before Fix
Disk Usage


95%


↓


Writes Slow


↓


Risk of Disk Full


↓


Possible Node Failure


After Fix
Removed Snapshots


↓


Extended Storage


↓


Added Node


↓


Disk Usage


60%

## Source PDF page 91

Cluster healthy again.


Complete Production Flow
Monitoring Alert
     │
     ▼
Disk = 95%
     │
     ▼
Run df -h
     │
     ▼
Disk Confirmed Full
     │
     ▼
Run du -sh /var/lib/cassandra/*
     │
     ▼
Find Large Snapshot Directory
     │
     ▼
Check Data Growth
     │
     ▼
Root Cause Found
     │
     ▼
Delete Old Snapshots
     │
     ▼
Extend Storage
     │
     ▼
Plan Capacity Expansion

## Source PDF page 92

      │
      ▼
Disk Usage Returns to Normal


Interview Answer (Senior DBA)
"We received a monitoring alert indicating one Cassandra node had reached
95% disk utilization. I first verified the filesystem usage using df -h, then
analyzed the Cassandra directories with du -sh /var/lib/cassandra/*. I found
that, besides normal data growth, old snapshots were consuming
approximately 50 GB of disk space. I confirmed this using nodetool
listsnapshots and removed obsolete snapshots with nodetool clearsnapshot
after ensuring they were no longer needed. Since the application data was
also growing rapidly, we extended the storage capacity and included
additional nodes in our capacity planning to distribute data more evenly.
After cleanup and expansion, disk utilization dropped to a safe level, and the
cluster continued operating normally."
Important Interview Follow-up
Interviewer:
"Can I delete SSTable files manually when disk is full?"
Correct Answer:
No.
Never delete files directly from:
/var/lib/cassandra/data
because it can corrupt the node or cause data inconsistency.
Safe options are:
   Remove only obsolete snapshots using nodetool clearsnapshot.
   Extend the filesystem or attach additional storage.
   Add new nodes and rebalance the cluster.
   Remove old backups or logs only after verifying they are no longer
    required.
This shows the interviewer that you understand both Cassandra internals and
safe production operations.

## Source PDF page 94

Scenario 8: Capacity Planning Problem
o   Storage usage increased by approximately 10 GB every day.
o   Investigation
o   Reviewed historical monitoring data for:
o   Storage growth
o   CPU utilization
o   Heap usage
o   Read/write throughput
o   Resolution
o   Forecasted storage growth, recommended adding new nodes before
    utilization exceeded 75–80%, and rebalanced the cluster.
o   Result
o   The cluster handled future growth without service disruption.
let me understand deeply pin to pin explain


Excellent. This is one of the most important Senior Cassandra DBA
interview questions because it tests whether you think proactively rather
than only reacting to incidents.
A good DBA doesn't wait for the disk to become full. They predict future
growth and take action before users are affected.
Let's understand this like a real production incident.


Production Scenario Monday Morning – Monthly Capacity Review
Your monitoring dashboard shows:
Storage Growth

Day 1 400 GB
Day 2 410 GB
Day 3 420 GB
Day 4 430 GB
Day 5 440 GB
Every day:
+10 GB

## Source PDF page 95

Application is working fine.
No alerts.
No incidents.
Question:
Should you wait until the disk reaches 100%?
No.
This is where Capacity Planning starts.


Step 1: What is Capacity Planning?
Capacity Planning means:
Predicting future resource requirements (Storage, CPU, Memory,
Network) before the system runs out of capacity.
Think of it like owning a water tank.
Suppose:
Tank Capacity
1000 Liters
Daily usage
100 Liters
Will you wait until the tank becomes empty?
No.
You'll refill it before that.
Exactly the same principle.


Step 2: First Investigation
Open monitoring dashboards.
You don't check only storage.
You also review:
      Storage growth
      CPU utilization
      Heap usage
      Read throughput
      Write throughput


Storage Growth

## Source PDF page 96

Suppose:
Date Used Storage
Jan 1 400 GB
Jan 2 410 GB
Jan 3 420 GB
Jan 4 430 GB
Jan 5 440 GB
Pattern:
10 GB/day
Question:
Will tomorrow be:
100 GB?
No.
Trend suggests:
450 GB


Step 3: Check CPU
Current:
CPU


45%
Good.
But monitoring history shows
Last month
25%
Now
45%
Traffic is increasing.


Step 4: Check Heap
Current

## Source PDF page 97

Heap


65%
Last Month
40%
Heap usage is increasing.
Application load is increasing.


Step 5: Check Read Throughput
Current
Read Requests


20,000/sec
Last Month
10,000/sec
Reads doubled.


Step 6: Check Write Throughput
Current
Writes


30,000/sec
Last Month
15,000/sec
Again doubled.
Everything indicates:
Business is growing.


Step 7: Calculate Future Storage
Suppose:
Today
500 GB
Daily growth
10 GB

## Source PDF page 98

Disk Size
1 TB
Question:
When will storage become full?
Simple Calculation
Free Space


1000 - 500


=


500 GB
Daily growth
10 GB
Days remaining
500 ÷ 10


=


50 Days
Meaning:
Within 50 days
↓
Disk Full.


Step 8: Why Not Wait 50 Days?
Because adding nodes is not instant.
You need:
       Change approval
       Procurement
       Maintenance window
       Cluster expansion
       Data streaming
       Application testing

## Source PDF page 99

This may take weeks.
So planning starts much earlier.


Step 9: Why 75–80%?
Interviewers often ask:
"Why do you recommend expansion at 75–80% instead of 95%?"
Suppose:
Disk Size
1000 GB
At 80%
800 GB Used
Remaining
200 GB
At 10 GB/day
You still have
20 Days
Enough time to:
       Order storage
       Add nodes
       Rebalance data
       Validate the cluster
If you wait until 95%:
950 GB Used
Only
50 GB
left.
That's just 5 days.
One unexpected spike could fill the disk before maintenance is completed.


Step 10: Resolution
Solution 1 – Add New Nodes
Current Cluster

## Source PDF page 100

3 Nodes


500 GB each
Total
1500 GB
Add
2 Nodes
Now
5 Nodes


500 GB each


=


2500 GB
Capacity increases.


Step 11: Why Rebalance?
After adding Node4
Initially
Node1


500 GB


Node2


500 GB


Node3


500 GB


Node4

## Source PDF page 101

0 GB
Node4 is empty.
Need streaming.
After rebalancing
Node1


375 GB


Node2


370 GB


Node3


380 GB


Node4


375 GB
Balanced cluster.


Step 12: Benefits
Before
Storage


80%


CPU


75%


Heap

## Source PDF page 102

70%
After adding node
Storage


55%


CPU


45%


Heap


55%
Every resource improves.


Why Did CPU Reduce?
More nodes means:
Application traffic
Before
3 Nodes
↓
30,000 Writes/sec
↓
10,000 Each
After
5 Nodes
↓
30,000 Writes/sec
↓
6,000 Each
Each node works less.
CPU drops.

## Source PDF page 103

Why Did Heap Reduce?
Each node stores less data.
Reads become smaller.
Less object creation.
Heap pressure decreases.


Complete Capacity Planning Flow
Business Growth
     │
     ▼
Daily Storage Growth
     │
     ▼
Review Historical Metrics
(Storage, CPU, Heap, Read/Write Throughput)
     │
     ▼
Predict Future Usage
     │
     ▼
Storage Will Reach 80%
     │
     ▼
Raise Capacity Request
     │
     ▼
Add New Nodes
     │
     ▼
Rebalance Data
     │
     ▼
Storage, CPU, Heap Return to Healthy Levels

## Source PDF page 104

Real Interview Conversation
Interviewer:
"How do you know when to add new Cassandra nodes?"
Good Answer:
"I don't wait until the cluster is full. I continuously monitor storage growth, CPU
utilization, heap usage, and read/write throughput using Grafana and
Prometheus. If I observe consistent growth trends and forecast that storage or
resource utilization will exceed 75–80% within the coming weeks, I initiate
capacity planning. This includes requesting additional nodes or storage,
scheduling cluster expansion, and rebalancing data before the cluster reaches a
critical state."


Senior DBA Interview Answer
"In one environment, storage usage was increasing by approximately 10 GB
every day. I analyzed historical trends using our monitoring dashboards and
confirmed that storage, CPU utilization, heap usage, and read/write throughput
were all steadily increasing. Based on the growth rate, I calculated when the
cluster would reach 80% and later 100% utilization. Instead of waiting for a
critical alert, I recommended adding new nodes before utilization exceeded 75–
80%. After the nodes were added, Cassandra streamed data to the new nodes,
the cluster was rebalanced, storage usage per node decreased, and CPU and
heap utilization also improved. This proactive capacity planning ensured the
cluster continued to support business growth without any service interruption."


Interview Tip
When answering capacity planning questions, always mention all four key
metrics, not just storage:
   1. Storage growth – How fast data is increasing.
   2. CPU utilization – Whether processing capacity is sufficient.
   3. Heap usage – Whether JVM memory is under pressure.
   4. Read/Write throughput – Whether workload growth requires additional
       nodes.
This demonstrates that you think like a production Cassandra DBA rather than
simply monitoring disk usage.

## Source PDF page 106

    11.         What are some common issues you have encountered while
       working with Cassandra?

    Answer:
    The interviewer is not asking for a list. They want to know:
    "Have you actually supported Cassandra in production?"
o   A strong answer explains:
o   The issue
o   How you investigated it
o   Root cause
o   Resolution
o   Result


Interview Question
    What are some common issues you have encountered while working
    with Cassandra?
    Sample Answer
o   "In my production experience, I have encountered several issues including
    high read latency, high write latency, tombstone problems, pending
    compactions, JVM garbage collection pauses, hot partitions, disk space
    issues, node failures, repair issues, and capacity planning challenges. For
    each issue, I first verify cluster health, analyze monitoring metrics, identify
    the root cause using Cassandra and Linux tools, implement corrective
    actions, and monitor the cluster until it stabilizes."


Common Production Issues
o   Issue                     o   Severity o     Common Root Cause
o   High Read Latency         o   High       o   SSTables, Tombstones
o   High Write Latency        o   High       o   Disk bottleneck
o   Pending Compactions       o   High       o   Heavy writes
o   GC Pauses                 o   High       o   Heap pressure
o   Hot Partition             o   High       o   Bad partition key
o   Disk Full                 o   Critical   o   Data growth

## Source PDF page 107

o   Issue                   o   Severity o     Common Root Cause
o   Node Down               o   Critical   o   Hardware/OS
o   ReadTimeoutException o      High       o   Tombstones
o   WriteTimeoutException o     High       o   Disk or network
o   Repair Failure          o   Medium o       Node down
o   Streaming Failure       o   Medium o       Network
o   Bootstrap Failure       o   Medium o       Disk/network
o   Schema Disagreement o       Medium o       Schema mismatch
o   High CPU                o   High       o   Hot partitions
o   High Heap Usage         o   High       o   Large queries
o   Now let's understand each one deeply.


Issue 1: High Read Latency
    Symptoms
o   Users report:
o   Application is slow while reading data.
o   Normally:
o   40 ms
o   Now:
o   3 Seconds
o   Investigation
o   nodetool status
    nodetool tablestats
    nodetool compactionstats
    iostat -x 1
o   Root Cause
o   Too many SSTables
o   Tombstones
o   Heavy compaction
o   Slow disk
o   Resolution
o   Optimize compaction

## Source PDF page 108

o   Reduce tombstones
o   Tune queries
o
o   Issue 2: High Write Latency
o   Symptoms
o   Insert operations become slow.
o   Investigation
o   nodetool tpstats


    nodetool compactionstats


    iostat -x 1
o   Root Cause
o   Disk cannot process writes fast enough.
o   Resolution
o   Add nodes
o   Increase storage bandwidth
o   Tune compactions


Issue 3: Pending Compactions
o   Symptoms
o   nodetool compactionstats
o   Shows
o   Pending Tasks


    500
o   Root Cause
o   Compactions cannot keep up with write traffic.
o   Resolution
o   Add nodes
o   Faster storage
o   Tune concurrent compactions
o
o   Issue 4: Tombstones

## Source PDF page 109

o   Symptoms
o   Application log
o   ReadTimeoutException
o   Investigation
o   nodetool tablestats
o   Root Cause
o   Large number of DELETE operations.
o   Very short TTL.
o   Resolution
o   Reduce TTL
o   Better schema
o   Allow compaction
o
o   Issue 5: JVM Garbage Collection
o   Symptoms
o   Application becomes slow randomly.
o   Investigation
o   nodetool gcstats
o   Heap
o   95%
o   Root Cause
o   Heap pressure.
o   Large queries.
o   Resolution
o   Tune heap
o   Tune G1GC
o   Reduce object creation
o
o   Issue 6: Hot Partition
o   Symptoms
o   Node1


    95% CPU
o   Other nodes

## Source PDF page 110

o   20%
o   Investigation
o   Review partition key.
o   Root Cause
o   Poor partition key.
o   Resolution
o   Redesign schema.
o
o   Issue 7: Disk Full
o   Symptoms
o   Disk reaches
o   95%
o   Investigation
o   df -h


    du -sh /var/lib/cassandra/*
o   Root Cause
o   Snapshots.
o   Rapid data growth.
o   Resolution
o   Remove old snapshots
o   Extend storage
o   Add nodes
o
o   Issue 8: Node Down
o   Symptoms
o   nodetool status
o   Shows
o   DN
o   Investigation
o   Check
o   systemctl status cassandra
o   Check
o   journalctl

## Source PDF page 111

o   Check logs.
o   Root Cause
o   Hardware failure
o   OS crash
o   JVM crash
o   Disk failure
o   Resolution
o   Restart.
o   Replace hardware.
o   Repair.
o
o   Issue 9: ReadTimeoutException
o   Symptoms
o   Application
o   ReadTimeoutException
o   Root Cause
o   Tombstones
o   Disk
o   Large partitions
o   Resolution
o   Reduce tombstones.
o   Tune queries.
o
o   Issue 10: WriteTimeoutException
o   Symptoms
o   WriteTimeoutException
o   Root Cause
o   Slow disk
o   Network latency
o   High write load
o   Resolution
o   Improve storage.
o   Check network.
o   Add nodes.

## Source PDF page 112

o
o   Issue 11: Repair Failure
o   Symptoms
o   Repair never completes.
o   Investigation
o   nodetool repair
o   Root Cause
o   Node unavailable
o   Network interruption
o   Resolution
o   Restore failed node.
o   Run repair again.
o
o   Issue 12: Bootstrap Failure
o   Symptoms
o   New node cannot join.
o   Investigation
o   Logs.
o   nodetool status
o   Root Cause
o   Network
o   Seeds
o   Disk
o   Resolution
o   Correct configuration.
o   Restart bootstrap.
o
o   Issue 13: Schema Disagreement
o   Symptoms
o   nodetool describecluster
o   Shows
o   Schema disagreement
o   Root Cause
o   One node has different schema.

## Source PDF page 113

o   Resolution
o   Wait for schema propagation.
o   Restart affected node if necessary.
o
o   Issue 14: High CPU
o   Symptoms
o   One node
o   95%
o   Investigation
o   Review data model.
o   Root Cause
o   Hot partitions.
o   Resolution
o   Redesign partition key.
o
o   Issue 15: Capacity Planning
o   Symptoms
o   Storage increasing
o   10 GB/day
o   Investigation
o   Review historical monitoring.
o   Resolution
o   Forecast growth.
o   Add nodes before reaching 80%.
o
o   Commands Every Cassandra DBA Should Know
o   nodetool status
    nodetool info
    nodetool tablestats
    nodetool tpstats
    nodetool gcstats
    nodetool compactionstats
    nodetool netstats
    nodetool repair

## Source PDF page 114

    nodetool cleanup
    nodetool drain
o   Linux:
o   df -h
    du -sh
    iostat -x 1
    vmstat
    top
    sar
    free -m


Best Interview Answer (3 Minutes)
"In my production experience, the most common Cassandra issues have been
high read latency, high write latency, pending compactions, tombstone
accumulation, JVM garbage collection pauses, hot partitions, disk utilization
issues, node failures, and capacity planning. Whenever an issue occurs, I first
verify cluster health using nodetool status, then analyze Cassandra metrics such
as tpstats, tablestats, gcstats, and compactionstats, along with Linux metrics
like disk I/O and CPU utilization. Based on the findings, I identify the root cause
and implement corrective actions such as optimizing the data model, tuning JVM
and compaction settings, expanding cluster capacity, or coordinating with
application teams for schema improvements. Finally, I validate the fix through
monitoring to ensure cluster performance and stability are restored."


o   This answer demonstrates production troubleshooting methodology,
    which is exactly what interviewers expect from a 4+ year Cassandra DBA.