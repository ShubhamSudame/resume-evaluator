// MongoDB initialization script for Resume Evaluator
// This script runs when the MongoDB container starts for the first time

// Switch to the resume_evaluator database
db = db.getSiblingDB('resume_evaluator');

// Create collections with validation
db.createCollection("job_descriptions", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: ["title", "description", "requirements"],
         properties: {
            title: {
               bsonType: "string",
               description: "Job title - required"
            },
            description: {
               bsonType: "string",
               description: "Job description - required"
            },
            requirements: {
               bsonType: "array",
               description: "Job requirements - required"
            }
         }
      }
   }
});

db.createCollection("resumes", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: ["filename", "content"],
         properties: {
            filename: {
               bsonType: "string",
               description: "Resume filename - required"
            },
            content: {
               bsonType: "string",
               description: "Resume content - required"
            }
         }
      }
   }
});

db.createCollection("evaluations", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: ["resume_id", "job_description_id"],
         properties: {
            resume_id: {
               bsonType: "objectId",
               description: "Resume ID - required"
            },
            job_description_id: {
               bsonType: "objectId",
               description: "Job Description ID - required"
            }
         }
      }
   }
});

// Create indexes for better performance
db.job_descriptions.createIndex({ "title": 1 });
db.job_descriptions.createIndex({ "created_at": -1 });

db.resumes.createIndex({ "filename": 1 });
db.resumes.createIndex({ "created_at": -1 });
db.resumes.createIndex({ "job_description_id": 1 });

db.evaluations.createIndex({ "resume_id": 1, "job_description_id": 1 });
db.evaluations.createIndex({ "created_at": -1 });

print("MongoDB initialization completed successfully!");
print("Collections created: job_descriptions, resumes, evaluations");
print("Indexes created for optimal performance"); 