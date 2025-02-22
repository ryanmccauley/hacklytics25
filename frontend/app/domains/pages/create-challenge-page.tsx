import { Button } from "~/components/ui/button"

export default () => {
  return (
    <div className="flex flex-col h-full items-center justify-center">
      <div className="bg-white max-w-4xl w-full rounded-lg shadow-sm border border-gray-200 p-8 flex flex-col space-y-4">
        <div className="flex flex-col">
          <h1
            className="text-2xl font-semibold tracking-tight"
          >
            InstantCTF
          </h1>
          <p>
            Create your own tailored CTF challenges in minutes
          </p>
        </div>
        <div className="flex flex-col space-y-2">
          <div className="flex flex-col">
            <h5>
              Challenge Category
            </h5>
          </div>
          <div className="flex flex-col">
            <h5>
              Challenge Difficulty
            </h5>
          </div>
          <div className="flex flex-col">
            <h5>
              Additional Information
            </h5>
          </div>
          <div className="flex items-center justify-end">
            <Button
              size="lg"
            >
              Create Challenge
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}