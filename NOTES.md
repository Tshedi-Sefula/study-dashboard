# 1. Schema

I designed the activities table as an event log where each row represents a single user action. This makes it easy to track behaviour over time and compute things like totals and averages when needed.

If the table grew to around 10 million rows, I would index student_id because most queries will filter by a specific student. I would also consider a composite index on student_id and activity_type since we often filter by type when calculating quiz scores. An index on created_at would also help for time-based filtering.

# 2. API

The /groups/{id}/stats endpoint calculates aggregates on the fly. If the table had a lot of data (like 100k+ activities) and this endpoint was called frequently, it would start to get slow because it has to recompute values every time.

To fix this, I would probably precompute the stats and store them, either in a separate table or a cached/materialized view. That way, the API just reads precomputed values instead of recalculating everything on each request.

# 3. Frontend

If the “Add activity” request fails, the user doesn’t really get clear feedback. From their point of view, they click submit and nothing changes, so it looks like the system is broken or slow.

Ideally, I would show an error message (like a small alert or toast) and keep the form values so the user can try again. Right now it’s not very clear whether the request failed or succeeded.

# 4. Bug hunt

There are a couple of issues in the snippet.

The first bug is that useEffect has no dependency array, so it runs on every render. Since it sets state, this causes repeated re-renders and continuous API calls. Adding a dependency array (like [studentId]) fixes this.

The second issue is that there is no error handling for the fetch call. If the request fails, the component won’t handle it properly and could stay stuck in a loading state. I would add a .catch() or switch to async/await with try/catch.

Also, data.activities is used without checking if it exists, which could cause a crash if the API response is missing that field.

# 5. Tradeoff & AI

Because of the time limit, I focused on getting the main flow working (viewing groups, listing students, and adding activities) instead of building more advanced features like caching, optimistic updates, or better state management.

If I had more time, I would improve the frontend data handling and probably add React Query to manage API calls properly. I would also improve error handling and loading states.

I used an AI tool to help set up the initial structure of the frontend and align it with the API. However, I had to change quite a bit because some of the endpoints and data shapes didn’t match the actual backend.