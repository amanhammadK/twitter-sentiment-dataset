import { z } from "zod";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_PATH = join(__dirname, "..", "data", "dataset.json");

export const TweetRecordSchema = z.object({
  id: z.string(),
  text: z.string(),
  sentiment: z.enum(["positive", "negative", "neutral"]),
  confidence: z.number().min(0).max(1),
  username: z.string().optional(),
  timestamp: z.string().optional(),
  likes: z.number().int().min(0).optional(),
  retweets: z.number().int().min(0).optional(),
  replies: z.number().int().min(0).optional(),
  hashtags: z.array(z.string()).optional(),
  brand: z.string().optional(),
  verified: z.boolean().optional(),
});

export const DatasetSchema = z.array(TweetRecordSchema);
export type TweetRecord = z.infer<typeof TweetRecordSchema>;

export function loadAndValidate(): { valid: TweetRecord[]; errors: z.ZodError[] } {
  const raw = JSON.parse(readFileSync(DATA_PATH, "utf-8"));
  const valid: TweetRecord[] = [];
  const errors: z.ZodError[] = [];
  for (const item of raw) {
    const result = TweetRecordSchema.safeParse(item);
    if (result.success) {
      valid.push(result.data);
    } else {
      errors.push(result.error);
    }
  }
  return { valid, errors };
}

export function validateRecord(record: unknown): record is TweetRecord {
  return TweetRecordSchema.safeParse(record).success;
}
